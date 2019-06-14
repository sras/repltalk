import neovim
import json
import http.client
import time

def build_error_list(items, file_map=None):
    ret = []
    for (idx, e) in enumerate(items['errors']):
        for (idx1, ln) in enumerate(e['text'].split('\n')):
            # We attach each line to the error, keeping the error no (nr) same for the
            # lines belonging to same error.
            if idx1 == 0:
                ret.append({'filename': apply_file_map(e['file_name'], file_map), 'lnum': e['line'], 'col': e['column'], 'text': ln, 'nr': idx, 'type': 'E'})
            else:
                ret.append({'text': ln, 'nr': idx, 'type': 'E'})

    for (idx, e) in enumerate(items['warnings']):
        for (idx1, ln) in enumerate(e['text'].split('\n')):
            if idx1 == 0:
                ret.append({'filename': apply_file_map(e['file_name'], file_map), 'lnum': e['line'], 'col': e['column'], 'text': ln, 'nr': idx, 'type': 'W'})
            else:
                ret.append({'text': ln, 'nr': idx, 'type': 'W'})
    return ret

def apply_file_map(path, file_map):
    if file_map is not None:
        for fromp in file_map:
            if path.startswith(fromp):
                return "{}{}".format(file_map[fromp], path[len(fromp):])
        return path
    else:
        return path

@neovim.plugin
class ReplTalk(object):
    def __init__(self, vim):
        self.vim = vim

    def repl_command(self, command, host, port):
        return self.send_req(host, port, "/command", {'command': command})

    def send_req(self, host, port, path, data = None):
        conn = http.client.HTTPConnection("{}:{}".format(host, port))
        if data:
            conn.request("POST", path, json.dumps(data), headers = {'Content-type': 'application/json'})
        else:
            conn.request("GET", path)
        res = conn.getresponse()
        return json.loads(res.read())

    def process_output(self, msg):
        if 'error' in msg:
            print(msg['error'])
        else:
            if len(msg['output']['errors']) > 0:
                self.vim.command('REPLTalkIndicateError')
            elif len(msg['output']['warnings']) > 0:
                self.vim.command('REPLTalkIndicateWarnings')
            else:
                self.vim.command('REPLTalkIndicateSuccess')
            try:
                file_map = self.vim.eval('g:REPLTALK_FILE_MAP')
            except:
                file_map = None
            elist = build_error_list(msg['output'], file_map=file_map)
            self.vim.funcs.setqflist([], 'r', {"items": elist, "title": "REPLTalk Error list"})

    @neovim.function('REPLTalkCommand', sync=False)
    def command_handler(self, args):
        try:
            r = self.repl_command(args[0], args[1], args[2])
        except:
            print("Connection/Decoding error, please start the REPLTalk server")
        if 'error' in r:
            if r['error'] == 'NOT_STARTED':
                self.process_output(self.send_req(args[1], args[2], '/start'))
                self.command_handler(args)
        else:
            self.process_output(r)
