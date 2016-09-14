#!/usr/bin/env python3

import malt
import malt.helpers as helpers
import malt.barbet as bar
import os

def main():
    options = [
        "add i:a, i:b",
        "int i:n",
        "kwargs one=1, two=2, three=3",
        "types s:str=string, i:int=5, f:float=1.0",
        "echo string",
        "load",
        "div s[top|bottom]:anchor",
    ]
    bar.set_footer(options)
    bar.render()
    while True:
        r = malt.offer(options)
        if r == 'add':
            bar.message("{} + {} = {}".format(r.a, r.b, r.a+r.b))

        elif r == 'int':
            bar.message(str(r.n) + str(type(r.n)))

        elif r == 'kwargs':
            bar.message(r)

        elif r == 'echo':
            bar.message(r.string)

        elif r == 'load':
            bar.message(malt.load('example.malt'))

        elif r.raw_head == 'clear':
            bar.clear()

        elif not r.empty:
            bar.message(r.error)
        bar.render()

if __name__ == '__main__':
    main()
    #malt.serve(malt.load('example.lang'))
