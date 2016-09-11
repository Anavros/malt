" Vim syntax file
" Language: Malt Config Grammar (.malt)

if exists("b:current_syntax")
    syntax clear
endif

syn match maltCommand "\v^[a-z]+"
syn match maltComment "\v#.*"
syn match maltSyntax "\v^\?.*"
syn match maltNumeral "\v[0-9]+\.[0-9]*"

syn region maltString start=+"+ end=+"+ skip=+\\"+

hi link maltCommand  Keyword
hi link maltComment  Comment
hi link maltString   String
hi link maltNumeral  Number
hi link maltSyntax   Special

let b:current_syntax = "malt"
