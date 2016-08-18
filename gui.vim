" Vim syntax file
" Language: Bot Grammar (.bot)

if exists("b:current_syntax")
    syntax clear
endif

syn keyword guiKeyword div
syn keyword guiAnchor top bottom left right

syn match guiComment "\v#.*"
syn match guiSyntax "\v^\?.*"
syn match guiNumeral "\v[0-9]+\.[0-9]*"

syn region guiFile start=+"+ end=+"+ skip=+\\"+

"syn match botToken "\v\{[a-z.#?:0-9_]+\}"
"syn match botDivider "\v:"
"syn match botWeight "\vx[0-9]+"
"syn match botOption "\v\([^()]*\)"
"syn match botTag "\v\+[a-z_0-9]+"

"syn match packToken "\v\^[a-z]+\^"
"syn match packCosmetic "\v\{[a-z]+\}"
"syn match packHeader "\v\[\-\s*[a-z]+\s*\-\]"
"syn match packHeader "\v\[\^\s*[a-z]+\s*\^\]"
"syn match packComment "\v#.*"
"syn match packColon "\v:\s*[a-z]"me=e-1


hi link guiKeyword  Keyword
hi link guiAnchor   Function
hi link guiComment  Comment
hi link guiFile     String
hi link guiNumeral  String
hi link guiSyntax   Special

let b:current_syntax = "gui"
