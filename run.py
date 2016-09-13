#!/usr/bin/env python3

import malt
import os

def main():
    options = [
        "add i:a, i:b",
        "int i:n",
        "kwargs one=1, two=2, three=3",
        "echo string",
        "load",
        "div s[top|bottom]:anchor",
    ]
    while True:
        r = malt.offer(options)
        if r == 'add':
            print("{} + {} = {}".format(r.a, r.b, r.a+r.b))

        elif r == 'int':
            print(r.n, type(r.n))

        elif r == 'kwargs':
            malt.serve(r)

        elif r == 'echo':
            malt.serve(r.string)

        elif r == 'load':
            malt.serve(malt.load('example.lang'))

        elif r.raw_head == 'clear':
            os.system('clear')

        elif not r.valid:
            malt.serve(r.raw_args)
            malt.serve(r.raw_kwargs)
            malt.serve(options)

if __name__ == '__main__':
    main()
    #malt.serve(malt.load('example.lang'))
