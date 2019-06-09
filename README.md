# ReplTalk - Talk to REPLs from code editors.

This is a python package that includes language servers made by wrapping corresponding REPLs and adaptors for various editors.

### Installing

```
pip3 install pyrepltalk
```

### Running

As of now, the following language Servers and Editor adapters are included.

Langage Servers: Haskell as `haskell_server`

Editor Adapters: Neovim as `neovim_adapter`, vim as `vim_adapter`. The adapter for Visual Studio Code is in the form of an Visual Studio Code extension.

### For Neovim

The plug-in for Neovim and Vim is one and the same and can be included with the following configuration (vim-plug plugin manager).

```
Plug 'sras/repltalk', { 'rtp': 'plugins/vim' }
```

The plug-in exports a function `REPLTalkCommand` that can be used to send commands to the adapter process. We can use this function to reload the modules on file save.
Add this line to your nvim configuration so that a reload command is sent to the repl when Haskell source files are saved.

```
  autocmd BufWritePost *.hs call REPLTalkCommand(":reload", 2096)
```

The adapter needs to know the RPC socket address of the Neovim process. This can be done via the `NVIM_LISTEN_ADDRESS` environment variable. If you are in a Neovim terminal,
then this variable will be preset by Neovim. If not, you can get it by `:echo v:servername` from Neovim. 

After you set the `NVIM_LISTEN_ADDRESS` in your terminal, go to your project folder and start the server for your language and Neovim adapter. For example, if you are using Haskell, that would be.

```
# export NVIM_LISTEN_ADDRESS=/tmp/nvimZiwKsm 
# haskell_server & nvim_adapter
```

Now, when you save .hs files in Neovim, you should see the GHCI process doing a reload. The adapter will populate the quickfix window and error list. You can open it in Neovim by using the `:copen` command.

In addition, Neovim and Vim adapters expects the following four vim commands pre-defined and available.

```
  REPLTalkIndicateError
  REPLTalkIndicateWarnings
  REPLTalkIndicateSuccess
  REPLTalkIndicateActivity
```

The adapters call these commands to indicate command status to the user in the editors.
The vim/neovim plugin already define these commands to change the status bar color. If you want to override this behavior, you can redefine what these commands do from configuration placed in the [after](http://vimdoc.sourceforge.net/htmldoc/options.html#after-directory) directory. Thus you can choose what happens in your editor at each stage of the command.

You can see the plug-in in action [here](https://youtu.be/iblExnkhy4s)

### For VIM

For VIM the communication with adapter has to be set up differently. The editor should be started by passing the `--servername` argument. The same name should be passed to the adapter through environment variable `VIM_SERVERNAME`.
Once this is setup, the server and adapter can be started.

```
# vim --servername SERVER
# export VIM_SERVERNAME=SERVER
# haskell_server & vim_adapter
```

You can see the plug-in in action [here](https://youtu.be/iblExnkhy4s)

### For Visual Studio Code

The Visual Studio Code extension does not require an adapter since JavaScript has got native support for async calls. So if you are using VSC, the you only have to start the REPL server.

Please refer to [this doc](https://github.com/sras/repltalk/tree/master/plugins/vsc).

A sample session can be seen [here](https://youtu.be/FgdxkvXk874).

### Port Numbers

The language servers run on port 2096 by default. Adapters on 2097. If you want to change this
set `LANGUAGE_SERVER_PORT` and `ADAPTER_PORT` environment variables.

### Language Server Interface

The language servers expose a simple web interface that exposes three endpoints.

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

Editor interface is same as the the server interface. But adaptors may not send the response back to the incoming request, and may directly communicate with the editors to pass the message to the user.
