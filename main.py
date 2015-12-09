#!/usr/bin/env python3

import malt


def main():
    #malt.show("Enter your name.")
    #name = malt.freeform()
    options = ["add n:int", "subtract", "halve", "double"]
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
            pass


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
