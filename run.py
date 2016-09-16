#!/usr/bin/env python3

import malt
import malt.helpers as helpers
import os

def main():
    options = [
        "add i:a, i:b",
        "int i:n",
        "kwargs one=1, two=2, three=3",
        "types s:str=string, i:int=5, f:float=1.0",
        "echo string",
        "load",
        "struct d:dict={k:v}, l:list=[1 2]",
        #"div s[top|bottom]:anchor",
    ]
    while True:
        r = malt.offer(options)
        if r == 'add':
            malt.serve("{} + {} = {}".format(r.a, r.b, r.a+r.b))

        elif r == 'int':
            malt.serve(str(r.n) + str(type(r.n)))

        elif r == 'kwargs' or r == 'struct':
            malt.serve(r)

        elif r == 'echo':
            malt.serve(r.string)

        elif r == 'load':
            malt.serve(malt.load('example.malt'))

        elif r.raw_head == 'clear':
            bar.clear()

        elif not r.empty:
            malt.serve(r.error)

if __name__ == '__main__':
    main()
