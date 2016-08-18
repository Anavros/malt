
import malt
import argparse

boilerplate = r"""
if exists("b:current_syntax")
    syntax clear
endif

syn keyword {lang}Keyword {keywords}
syn keyword {lang}AllowedValue {values}

syn match {lang}Comment "\v#.*"
syn match {lang}Syntax "\v^\?.*"
syn match {lang}Numeral "\v[0-9]+\.[0-9]*"

syn region {lang}Quote start=+"+ end=+"+ skip=+\\"+

hi link {lang}Keyword       Keyword
hi link {lang}AllowedValue  Function
hi link {lang}Comment       Comment
hi link {lang}Quote         String
hi link {lang}Numeral       Constant
hi link {lang}Syntax        Special

let b:current_syntax = "{lang}"
"""

def main(args):
    allowed_syntaxes = malt._read_syntax_comments(args.path)
    keywords = []
    values = []
    for (cmd, params) in allowed_syntaxes:
        keywords.append(cmd)
        for p in params:
            if p.values:
                values.extend(p.values)
    keys = ' '.join(keywords)
    vals = ' '.join(values)
    output = boilerplate.format(lang=args.name, keywords=keys, values=vals)
    with open(args.out_path, 'w') as f:
        print(output, file=f)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("out_path")
    parser.add_argument("-n", "--name", default="maltsyn")
    main(parser.parse_args())
