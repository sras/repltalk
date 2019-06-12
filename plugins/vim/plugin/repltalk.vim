function! REPLTalkCommand(command, port)
try

python3 << en
import vim
import json
import http.client
port = vim.eval("a:port")
data = {'command': vim.eval("a:command")}
conn = http.client.HTTPConnection("localhost:{}".format(port))
conn.request("POST", '/command', json.dumps(data), headers = {'Content-type': 'application/json'})
en
catch

python << en
import vim
import json
import httplib

port = vim.eval("a:port")
data = {'command': vim.eval("a:command")}
conn = httplib.HTTPConnection("localhost:{}".format(port))
conn.request("POST", '/command', json.dumps(data), headers = {'Content-type': 'application/json'})
en
endtry
endfunction

