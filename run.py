#!/usr/bin/env python3

import malt

def main():
    options = [
        "add int(n) int(m)",
        "dashes",
        "echo string",
        "load",
        "div anchor[top|bottom]"
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
    main()
