from repltalk import baseadapter
from repltalk.adapters import vim
import os

try:
    from pynvim import attach, NvimError
except ImportError:
    print("You need 'neovim' python library to run this adapter. Please install it using pip")

def get_nvim():
    return attach('socket', path=get_nvim_address())

def get_nvim_address():
    return os.environ['NVIM_LISTEN_ADDRESS']

def call_vim_function(fnc, nvim):
    try:
        nvim.call(fnc)
    except NvimError as e:
        print("Warning: No function {} defined in Neovim.".format(fnc))

def call_vim_command(fnc, nvim):
    try:
        nvim.command(fnc)
    except NvimError as e:
        print("Warning: No command {} defined in Neovim.".format(fnc))

nvim = get_nvim()

class NVIM(baseadapter.BaseAdapter):
    def show_activity(self):
        call_vim_command('REPLTalkIndicateActivity', nvim)

    def send_result(self, msg):
        try:
            elist = vim.build_error_list(msg['output'], vim.get_file_mapping())
            if len(msg['output']['errors']) > 0:
                call_vim_command('REPLTalkIndicateError', nvim)
            elif len(msg['output']['warnings']) > 0:
                call_vim_command('REPLTalkIndicateWarnings', nvim)
            else:
                call_vim_command('REPLTalkIndicateSuccess', nvim)
            nvim.call('setqflist', [], 'r', {"items": elist, "title": "REPLTalk Error list"})
        except Exception as e:
            print("Caught exception {}".format(e))
            pass

def main():
    NVIM()
