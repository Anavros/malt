#!/usr/bin/env python3

import single as malt

def main():
    options = [
        "add n:int m:int",
#        """add #'add two numbers together.'
#        n:int #'one number'
#        m:int #'another number'
#        """
        "subtract",
        "echo string",
        "load"
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
            filename = 'example.lang'
            options = [
                "div id anchor:str(top|bottom|left|right) texture size:float"
            ]
            malt.serve(malt.harvest(filename, options=None))

if __name__ == "__main__":
    main()
