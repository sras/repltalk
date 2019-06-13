function! ProcessResponse(channel)
  let full_msg = ""
  while ch_status(a:channel, {'part': 'out'}) == 'buffered'
    let full_msg = full_msg . ch_read(a:channel)
  endwhile
python << en
import json
import vim

def parse_result(resp):
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

if len(msg['output']['errors']) > 0:
    vim.command('REPLTalkIndicateError')
elif len(msg['output']['warnings']) > 0:
    vim.command('REPLTalkIndicateWarnings')
else:
    vim.command('REPLTalkIndicateSuccess')

try:
    file_map = vim.eval('g:REPLTALK_FILE_MAP')
except:
    file_map = None

elist = build_error_list(msg['output'], file_map=file_map)
setfqlist = vim.Function('setqflist')
setfqlist([], 'r', {"items": elist, "title": "REPLTalk Error list" + str(file_map)}  )
en
endfunction

function REPLTalkCommand(command, port)
  let js = ["curl", "--header", "Content-Type: application/json", "--request", "POST","--data", json_encode({"command":a:command}),  "http://localhost:".string(a:port)."/command"]
  call job_start(js, {'close_cb': 'ProcessResponse'})
endfunc

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
