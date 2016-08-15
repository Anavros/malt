
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
cmd arg:str
bad arg:badtype
cmd arg1 arg2
cmd arg_one arg_two arg_three
bad:str
bad:badtype
bad(a|b|c)
cmd arg:str(a|b)
bad arg(a|b)
*** arg
cmd ***
cmd ::: &&&
-u-"""

red = '\033[31m'
green = '\033[32m'
stop = '\033[0m'

line_form = r"""
^
(?P<cmd> \w+)               # Required command name.
(?P<args> \s[\w|:()]+)*     # Zero or more optional arguments. Refined later.
$
"""

word_form = r"""
^
(?P<key> \w+)               # \1 Required argument name.
(?P<cast> :(str|int|float)   # \2 Optional type specifier separated by a colon.
(?P<allow> \([a-z_|0-9]*\)    # \3 Optional pipe-separated list of allowed values.
)?
)?
$
"""

def val():
    os.system("clear")
    for line in lines.split('\n'):

        line_match = re.fullmatch(line_form, line, re.VERBOSE)
        if not line_match:
            print(line, red, False, stop)
        else:
            cmd = line_match.group('cmd')
            args = line_match.group('args')
            if args:
                for word in args.split():
                    word_match = re.fullmatch(word_form, word, re.VERBOSE)
                    if not word_match:
                        print(line, red, False, stop)
                    else:
                        print(line, green, True, stop)
            else:
                print(line, green, True, stop)

val()
