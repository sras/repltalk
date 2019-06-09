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

command! REPLTalkIndicateError call REPLTalkIndicateError()
command! REPLTalkIndicateWarnings call REPLTalkIndicateWarnings()
command! REPLTalkIndicateSuccess call REPLTalkIndicateSuccess()
command! REPLTalkIndicateActivity call REPLTalkIndicateActivity()
