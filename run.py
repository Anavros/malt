#!/usr/bin/env python3

import test as malt

def main():
    options = [
        "add int(n) int(m)",
        "dashes",
        "echo string",
        "load",
        "div anchor[top|bottom]"
    ]
    new_options = [
        "add i:n, i:m",
        "dashes",
        "echo string",
        "load",
        "div s[top|bottom]:anchor",
    ]
    while True:
        response = malt.offer(options) 
        if response == "add":
            malt.serve(response.n + response.m)

        elif response == "subtract":
            malt.serve("---")

        elif response == "echo":
            malt.serve(response.string)

        elif response == "load":
            malt.serve(malt.load('example.lang'))

if __name__ == "__main__":
    #main()
    malt.serve(malt.load('example.lang'))
