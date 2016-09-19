#!/usr/bin/env python3

import malt
import malt.bar as bar
import malt.helpers as helpers
import os

# malt.use_frontend('fancy')
# but what about extra functions? just no-op them?

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
        "multiline",
        "struct d:dict={k:v}, l:list=[1 2]",
        "dict d(s:i):arg={}",
        "len l(2):two, l(2:4):twofour",
        "div s(top|bottom):anchor",
        "baddiv s:anchor",
    ]
    #(1:5)  # only two
    #(1|2|3|4|5)  # any number
    while True:
        r = malt.offer(options)
        if r == 'load':
            malt.serve(malt.load('items.malt'))
        if r.valid:
            malt.serve("success!")
            malt.serve(r)
        else:
            malt.serve("failure.")
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
