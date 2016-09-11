
import re 
import os

words = [
    "arg",
    "arg:badtype",
    "arg4:str",
    "5arg:int",
    "_arg:float",
    "arg_arg2",
    "anchor:str(top|bottom)",
    "b**t",
    "this:t^&p",
    "this:is:bad:(as|well)",
    "mal:form(ed|ing)",
    "bad(type)",
    "good:str(val)",
]

lines = r"""cmd
cmd arg
cmd (butts)
cmd str(arg)
bad badtype(arg)
cmd arg1 arg2
cmd arg_one arg_two arg_three
str(bad)
badtype(bad)
bad[a|b|c]
cmd arg[a|b]
*** arg
cmd ***
cmd ::: &&&
-u-"""

pylines = r"""cmd
cmd i:n
cmd thing_1, thing_b, f:n, i:i, s:thing
cmd s[one|two|three]:n
cmd i:n, i:m
cmd i:n=1, string=butt
bad thing_1 thing_b f:n i:i s:thing
bad thing:butt
bad thing:[set|of|these]
bad int(y)"""

red = '\033[31m'
green = '\033[32m'
stop = '\033[0m'

word_form = r"""
^
(?P<cast>(str|int|float))?
 (?(cast) \( )
(?P<key>[a-z]+)
 (?(cast) \) )
(?P<allow>\[[\w\d_|]+\])?
$
"""

python_form = r"""
^
(?P<mod>[isf])?
 (?(mod)(?P<lim>\[[\w|]+\]))?
 (?(mod):)
(?P<key>[\w]+)
(?P<def>=[\w]+)?
$
"""

python_line = r"""
^
(?P<head>[\w]+)
(?P<tail>\s+[\w\s|:=,\[\]]+)*
$
"""

def val():
    os.system("clear")
    for line in pylines.split('\n'):
        line_match = re.fullmatch(python_line, line, re.X)
        success = True
        if not line_match:
            show(line, extra='bad line')
            continue
        head = line_match.group('head')
        tail = line_match.group('tail')
        if tail is None:
            show(line, True)
            continue
        for word in tail.split(','):
            match = re.fullmatch(python_form, word.strip(), re.X)
            if not match:
                success = False
                break
        if success:
            show(line, True)
        else:
            show(line)


def show(line, x=False, extra=""):
    print(green if x else red, line, '('+extra+')', stop)

val()
