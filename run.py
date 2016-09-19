#!/usr/bin/env python3

import malt
import malt.helpers as helpers
import os


def main():
    options = [
        "add i:a, i:b",
        "int i:n",
        "lim_int i(1:10):n",
        "float f(0.0:1.0):n",
        "kwargs one=1, two=2, three=3",
        "types s:str=string, i:int=5, f:float=1.0",
        "echo string",
        "load",
        "line",
        "struct d:dict={k:v}, l:list=[1 2]",
        "dict d(s:i):arg={}",
        "len l(2):two, l(2:4):twofour",
        "div s(top|bottom):anchor",
        "baddiv s:anchor",
        "bless",
        "revert",
    ]
    #(1:5)  # only two
    #(1|2|3|4|5)  # any number of options
    while True:
        malt.clear('head')
        malt.clear('foot')
        malt.clear('side')
        malt.serve('this goes in the head', to='head')
        malt.serve('this goes in the foot', to='foot')
        malt.serve('this goes in the side', to='side')
        r = malt.offer(options)
        if r == 'load':
            malt.serve(malt.load('items.malt'))
        elif r == 'bless':
            malt.bless()
        elif r == 'revert':
            malt.revert()
        elif r == 'line':
            malt.serve("this\nline\nis\nseparated\nby\nnew\nlines")
            with malt.indent():
                malt.serve("Hello, there!")
                with malt.indent():
                    malt.serve("I'm indented!")
        #if r.valid:
            #malt.serve("success!")
            #malt.serve(r)
        else:
            #malt.serve("failure.")
            helpers.try_extra_functions(r, options)


if __name__ == '__main__':
    main()
