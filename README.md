# REPL To Language Server

This is a python package that includes language servers made by wrapping corresponding REPLs and adaptors for various editors.

# Language Server Interface

The language servers expose a simiple web interface that exposes three endpoints.

## GET /start

Starts the repl process and responds with the output until the first prompt

## GET /stop

Kills the repl process

## POST /command

include the command to be executed in the request body in json format json {'command': command-to-execute }.

responds with output from repl in format { 'output': output-from-repl-during-command }. If there was an
error, the response would be {'error': error-description }.

# Editor Adapter interface

Editor interface is same as the the server interface. But adaptors may not send the response back to the incoming
request, and may instead directly communicate with the editors to pass the message to the user.

As of now, the following language Servers and Editor adapters are included.

Langage Servers: Haskell

Editor Adapters: Neovim, vim
