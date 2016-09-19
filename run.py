#!/usr/bin/env python3

import malt
import malt.bar as bar
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
        "multiline",
        "struct d:dict={k:v}, l:list=[1 2]",
        #"div s[top|bottom]:anchor",
        "div o(top|bottom):anchor",
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

        elif r == 'div':
            malt.serve(r)

        else:
            helpers.try_extra_functions(r, options)


def test_bar():
    options = [
        'single',
        'multi',
    ]
    bar.head("Header")
    bar.foot("Footer")
    bar.render()
    quitting = False
    while not quitting:
        response = malt.offer(options)
        if response == 'single':
            bar.slide("This is a single line!")
        elif response == 'multi':
            bar.slide("This one\nstretches\nacross\nmultiple lines\nhooray.")
        elif response.raw_head == 'clear':
            bar.clear()
        elif response.raw_head == 'quit':
            quitting = True
        bar.render()

if __name__ == '__main__':
    main()
    #test_bar()
