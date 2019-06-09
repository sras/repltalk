# Repltalk extension for Visual Studio Code

## Installing

You have to install the npm tool `vsce` to package this code as an Extension.

```
npm install -g vsce
```

Then change directory to `plugins/vsc` folder inside this repo and run `vsce` package command to generate a `.vsix` file.

```
vsce package
```

Now you can install this extension from Visual Studio Code interface by the "Install extension from vsix file" option.

## Running

Once you install the extension, you can activate it by selecting "Repl Talk" from the `Ctrl-Shift-p` menu.
Before that, you have to start the `repltalk` server in your project's root folder. It does not matter if the terminal is
one inside the Visual Studio Code or one out of it.

## Operation

When you activate the extension, it sends a `start` call to the repl server. This starts the wrapped `stack ghci` process
and the output starts to appear in the terminal. After this, for every file save, a `reload` command will be sent to the server.
The response from this call will appear as notification messages and items in the problems pane of the editor.

A sample session can be seen [here](https://youtu.be/FgdxkvXk874).
