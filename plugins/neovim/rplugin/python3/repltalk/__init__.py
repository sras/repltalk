import neovim

@neovim.plugin
class Limit(object):
    def __init__(self, vim):
        self.vim = vim
        self.calls = 0

    @neovim.command('Cmd', range='', nargs='*', sync=True)
    def command_handler(self, args, range):
        self._increment_calls()
        self.vim.current.line = (
            'Command: Called %d times, args: %s, range: %s' % (self.calls,
                                                               args,
                                                               range))

    @neovim.autocmd('BufWritePost', pattern='*', sync=True)
    def autocmd_handler(self):
        self.vim.command("echo 123")
        self.vim.api.setqflist([], 'r', [])

    @neovim.function('Func')
    def function_handler(self, args):
        pass

    def _increment_calls(self):
        pass
