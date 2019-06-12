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

function! ProcessResponse(channel)	
  let full_msg = ""
  while ch_status(a:channel, {'part': 'out'}) == 'buffered'
    let full_msg = full_msg . ch_read(a:channel)
  endwhile
python << en
import json
import vim

def parse_result(resp):
  print(resp)
  return json.loads(resp)

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

msg = parse_result(vim.eval("full_msg"))
print(msg)

if len(msg['output']['errors']) > 0:
    vim.command('REPLTalkIndicateError')
elif len(msg['output']['warnings']) > 0:
    vim.command('REPLTalkIndicateWarnings')
else:
    vim.command('REPLTalkIndicateSuccess')

elist = build_error_list(msg['output'])
setfqlist = vim.function('setqflist')
setfqlist([], 'r', {"items": elist, "title": "REPLTalk Error list"})

en
endfunction
let js = ["curl", "--header", "Content-Type: application/json", "--request", "POST","--data", "{\"command\":\":reload\"}", "http://localhost:2096/command"]
call job_start(js, {'close_cb': 'ProcessResponse'})
