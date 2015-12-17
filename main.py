#!/usr/bin/env python3

import malt


def main():
    options = ["add n:int", "subtract", "halve", "double", "echo string"]
    while True:
        response = malt.select(options) 
        if response == malt.BACK_CODE:
            malt.show("Are you sure you would like to exit?")
            if malt.confirm():
                return

        elif response == "add":
            malt.show(response.n)

        elif response == "subtract":
            malt.show("---")

        elif response == "halve":
            pass

        elif response == "double":
            malt.show("This is a really, really, really long string that I want to "
            + "print out to the console and honestly I'm not sure just how long I can "
            + "make this thing.")

        elif response == "echo":
            malt.show(response.string)


def register():
    users = {}
    register_options = ['add name:str age:int', 'remove name:str', 'check'] 
    #malt._ultra_parse(register_options)
    while True:
        response = malt.ultra_select(register_options)
        if response == malt.BACK_CODE:
            return
        elif response == 'add':
            malt.show(response.name)
            malt.show(response.age)
            malt.show(response)
        elif response == 'remove':
            malt.show(response)
        elif response == 'check':
            argdict = malt._ultra_parse(register_options)
            malt.show(dict(argdict))
            malt.show(malt._replace_casts(dict(argdict)))

def display():
    pass

if __name__ == "__main__":
    main()
