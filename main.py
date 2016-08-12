#!/usr/bin/env python3

import single as malt

def main():
    options = [
        "add n:int m:int",
        "subtract",
        "echo string"
    ]
    while True:
        response = malt.offer(options) 
        if response == "add":
            malt.serve(response.n + response.m)

        elif response == "subtract":
            malt.serve("---")

        elif response == "echo":
            malt.serve(response.string)

if __name__ == "__main__":
    main()
