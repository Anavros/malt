
if exists("b:current_syntax")
    syntax clear
endif

syn keyword exampleKeyword div but tex
syn keyword exampleAllowedValue top bottom left right

syn match exampleCast "\v(str|float|int)\("me=e-1
syn match exampleDelimiter "\v[|()?]"
syn match exampleDelimiter "\v\["
syn match exampleDelimiter "\v\]"

syn match exampleComment "\v#.*"
syn match exampleSyntax "\v^\?.*" contains=exampleCast,exampleDelimiter,exampleAllowedValue,exampleKeyword
syn match exampleNumeral "\v[0-9]+\.[0-9]*"


syn region exampleQuote start=+"+ end=+"+ skip=+\\"+

hi link exampleKeyword      Keyword
hi link exampleAllowedValue Function
hi link exampleComment      Comment
hi link exampleQuote        String
hi link exampleNumeral      Constant
hi link exampleSyntax       Type
hi link exampleCast         Special
hi link exampleDelimiter    Normal

let b:current_syntax = "example"
