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
