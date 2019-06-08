# ReplTalk - Talk to REPLs from code editors.

This is a python package that includes language servers made by wrapping corresponding REPLs and adaptors for various editors.

### Installing

```
pip3 install pyrepltalk
```

### Running

As of now, the following language Servers and Editor adapters are included.

Langage Servers: Haskell as `haskell_server`

Editor Adapters: Neovim as `neovim_adapter`, vim as `vim_adapter`

So if you are using Haskell with Neovim editor you can start the server and adapter as follows.

```
  haskell_server & nvim_adapter
```

To kill it, just press Ctrl-C. Then use the `fg` command to bring the language server process to foreground, and you can kill it via Ctrl-C too.

### Port Numbers

The language servers run on port 2096 by default. Adapters on 2097. If you want to change this
set `LANGUAGE_SERVER_PORT` and `ADAPTER_PORT` environment variables.

### Language Server Interface

The language servers expose a simiple web interface that exposes three endpoints.

#### GET /start

Starts the repl process and responds with the output until the first prompt

#### GET /stop

Kills the repl process

#### POST /command

Include the command to be executed in the request body in json format, `{'command': command-to-execute }`.  
responds with output from repl in format `{ 'output': output-from-repl-during-command }`. If there was an
error, the response would be `{'error': error-description }`. You should also include the proper content type header for json when you are hitting this endpoint.

```'Content-type': 'application/json'```

### Editor Adapter interface

Editor interface is same as the the server interface. But adaptors may not send the response back to the incoming request, and may or may not directly communicate with the editors to pass the message to the user.

### Configuration for Vim and NeoVim

The adapters for NeoVim and Vim indicate compilation status in editor and populate the quickfix list with errors or warnings.

For neovim the `NVIM_LISTEN_ADDRESS` environment variable should be set to pass the neovim RPC port. If you are in a shell inside the neovim editor, this variable is probable set already by neovim. If not, you can get it by `:echo v:servername` from neovim.

For vim, the editor should be started by passing the `--servername` argument. The same name
should be passed to the adapter through environment variable `VIM_SERVERNAME`.

Neovim and Vim adapters expects four vim functions pre-defined and available. The adapters call these functions to indicate command status in the editors. Thus you can choose what happens in your editor at each stage of the command. These functions are the following.

```
  REPLTalkIndicateError

  REPLTalkIndicateWarnings

  REPLTalkIndicateSuccess

  REPLTalkIndicateActivity
```

A sample vim/neovim configuration that defines the above functions (changes status bar color to indicate status) and also sets the auto commands to send a
reload command to the adapters can be seen below.

```
  function! REPLTalkCommand(command, port)
  try

  python3 << en
  import vim
  import json
  import http.client
  port = vim.eval("a:port")
  conn = http.client.HTTPConnection("localhost:{}".format(port))
  data = {'command': vim.eval("a:command")}
  conn.request("POST", '/command', json.dumps(data), headers = {'Content-type': 'application/json'})
  en
  catch

  python << en
  import vim
  import json
  import httplib

  port = vim.eval("a:port")
  conn = httplib.HTTPConnection("localhost:{}".format(port))
  data = {'command': vim.eval("a:command")}
  conn.request("POST", '/command', json.dumps(data), headers = {'Content-type': 'application/json'})
  en
  endtry
  endfunction

  function! REPLTalkIndicateError()
    hi StatusLine ctermfg=black guibg=black ctermbg=DarkRed guifg=#fc4242
  endfunction

  function! REPLTalkIndicateWarnings()
    hi StatusLine ctermfg=black guibg=black ctermbg=gray guifg=#84ff56
  endfunction

  function! REPLTalkIndicateSuccess()
    hi StatusLine ctermfg=black guibg=black ctermbg=white guifg=#087e3b
  endfunction

  function! REPLTalkIndicateActivity()
    hi StatusLine ctermfg=black guibg=black ctermbg=Brown guifg=orange
  endfunction

  command! HLiveCompile call SetLiveCompile(1)
  command! HNoLiveCompile call SetLiveCompile(0)

  autocmd BufWritePost *.hs call ReloadHaskell()

  function! SetLiveCompile(lc)
    let g:live_compile = a:lc
  endfunction

  function! ReloadHaskell()
    if exists("g:live_compile") && g:live_compile == 1
      call REPLTalkCommand(":reload", 2097)
    endif
  endfunction
```

Call the `HLiveCompile` command and `HNoLiveCompile` commands to enable or disable auto reloading on file save.
