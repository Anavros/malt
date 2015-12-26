#!/usr/bin/env python3

import malt

def main():
    options = ["add n:int m:int", "subtract", "halve", "double", "echo string"]
    while True:
        response = malt.select(options) 
        if response == 'back':
            malt.show("Are you sure you would like to exit?")
            if malt.confirm():
                return

        elif response == "add":
            malt.show(response.n + response.m)

        elif response == "subtract":
            malt.show("---")

        elif response == "halve":
            with malt.indent():
                malt.serve("I'm indented!")
                malt.fill(['test'])
                with malt.indent():
                    malt.serve("Me too!")
                    malt.fill(['test'])
                    with malt.indent():
                        malt.serve("That makes three of us!")
                        malt.fill(['test'])

        elif response == "double":
            malt.show("This is a really, really, really long string that I want to "
            + "print out to the console and honestly I'm not sure just how long I can "
            + "make this thing.")

        elif response == "echo":
            malt.show(response.string)

if __name__ == "__main__":
    malt.PREFIX = '[main] '
    malt.INDENT_WIDTH = 4
    malt.OVERFLOW = 40
    main()
