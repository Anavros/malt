
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

def val():
    os.system("clear")
    for line in lines.split('\n'):
        success = True
        for word in line.split():
            match = re.fullmatch(word_form, word, re.X)
            if not match:
                success = False
                break
        if success:
            print(line, green, True, stop)
        else:
            print(line, red, False, stop)

val()
