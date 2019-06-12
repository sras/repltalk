# ReplTalk - Talk to REPLs from code editors.

This is a python package that includes language servers made by wrapping corresponding REPLs and plugins for various editors.

### Installing

```
pip3 install pyrepltalk
```

#### Starting the server

We will use the Haskell server here.

Open a terminal, and from your project folder, run

```
haskell_server
```

This starts the server at the default port 2096. If you want to use a different port
specify it using the `LANGUAGE_SERVER_PORT` environment variable before running the server.
Any arguments that you pass to `haskell_server` will be forwarded to wrapped REPL process.

```

```

### Editor Plugins

#### Neovim

If you are using vim-plug then add the following to the plugin configuration

```
Plug 'sras/repltalk', { 'rtp': 'plugins/neovim', 'do': ':UpdateRemotePlugins' }
```

After running `PlugInstall` restart the editor.

#### VIM

```
Plug 'sras/repltalk', { 'rtp': 'plugins/vim'}
```

Plugin should be usable after running `PlugInstall`.

### Visual Studio Code

First install the `vsce` tool.

```
npm install -g vsce
```

Then change directory to `plugins/vsc` folder in this repo and run `vsce package` command to generate a `.vsix` file.

```
cd plugins/vsc
vsce package
```


This will create a .vsix extension file that you can install from Visual Studio Code's user interface by selecting the "Install extension from vsix file" option from extensions menu.

## Running

Once you install the extension, you can activate it by selecting "Repl Talk" from the `Ctrl-Shift-p` menu.
Before that, you have to start the language server in your project's root folder. It does not matter if the terminal is
one inside the Visual Studio Code or one out of it.

## Operation

When you activate the extension, it sends a `start` call to the repl server. This starts the wrapped repl process
and the output starts to appear in the terminal. After this, for every file save, a `reload` command will be sent to the server.
The response from this call will appear as notification messages and as items in the problems pane of the editor.

A sample session can be seen [here](https://youtu.be/FgdxkvXk874).
