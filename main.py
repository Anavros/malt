#!/usr/bin/env python3

import malt


def main():
    #malt.show("Enter your name.")
    #name = malt.freeform()
    options = ["add", "subtract", "halve", "double"]
    while True:
        action = malt.select(options) 
        if action == malt.BACK_CODE:
            malt.show("Are you sure you would like to exit?")
            if malt.confirm():
                return

        elif action == "add":
            pass

        elif action == "subtract":
            pass

        elif action == "halve":
            pass

        elif action == "double":
            pass


def register():
    register_options = ['add name:str age:int', 'remove name:str'] 
    malt._ultra_parse(register_options)


def display():
    pass

if __name__ == "__main__":
    #main()
    register()
