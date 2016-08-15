
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

red = '\033[31m'
green = '\033[32m'
stop = '\033[0m'

def val(f):
    os.system("clear")
    print(f)
    for w in words:
        if re.match(f, w):
            print(w, green, True, stop)
        else:
            print(w, red, False, stop)
