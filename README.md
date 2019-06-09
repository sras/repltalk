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

### Editor configurations

This repo includes for Neovim, vim and Visual Studio Code.

### Configuration for Vim and NeoVim

The plugin for Neovim and vim is one and the same and can be included with the following configuration (vim-plug plugin manager).

```
Plug 'sras/repltalk', { 'rtp': 'plugins/vim' }
```

The plugin exports a function `REPLTalkCommand` that can be used to send commands to the repl process. We can use this function to reload the modules on file save.
Add this line to your vim/nvim configuration so that a reload command is sent to the repl when haskell source files are saved.

```
  autocmd BufWritePost *.hs call REPLTalkCommand(":reload", 2096)
```

In addition, the adapters for NeoVim and Vim indicate compilation status in editor and populate the quickfix list with errors or warnings.

For neovim the `NVIM_LISTEN_ADDRESS` environment variable should be set to pass the neovim RPC port. If you are in a shell inside the neovim editor, this variable is probable set already by neovim. If not, you can get it by `:echo v:servername` from neovim.

For vim, the editor should be started by passing the `--servername` argument. The same name
should be passed to the adapter through environment variable `VIM_SERVERNAME`.


Neovim and Vim adapters expects the following four vim commands pre-defined and available.

```
  REPLTalkIndicateError
  REPLTalkIndicateWarnings
  REPLTalkIndicateSuccess
  REPLTalkIndicateActivity
```

The adapters call these functions to indicate command status to the user in the editors.
The vim/neovim plugin already define these commands to change the status bar color. If you want to overrride this behavior, you can redefine what these commands do from configuration placed in the [after](http://vimdoc.sourceforge.net/htmldoc/options.html#after-directory) directory. Thus you can choose what happens in your editor at each stage of the command.

You can see the plugin in action [here](https://youtu.be/iblExnkhy4s)

### Visual Studio Code

Please refer to [this doc](https://github.com/sras/repltalk/tree/master/plugins/vsc).
