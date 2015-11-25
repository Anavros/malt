# coding=utf-8

# Malt
# boilerplate for interactive text loops in the console

import pprint
pp = pprint.PrettyPrinter()

# NEEDS:
#   bad input validation
#   number input
#   message on bad input
def limited_input(options, inFn=input):
    """Get one of a limited set of commands from the user.
    Return None if given bad input; e.g. an empty list or a scalar.
    """
    
    if (type(options) is not list) or (len(options) < 1):
        return None
    
    string = ""
    lc_options = [x.lower() for x in options]

    while not (string.lower() in lc_options):
        string = inFn().strip().lower()

        if (string == "help") and ("help" not in lc_options): 
            say("Malt: Help")
            say("possible commands are: ")
            say(options) # XXX
        elif string in lc_options:
            break

    return string


def confirm(string):
    """Ask the user to confirm a yes or no decision using the prompt."""


def say(stuff):
    """Print text to the console.
    Questionable usefulness over print.
    May be upgraded using pprint in the future.
    """

    if type(stuff) is str:
        print(stuff)
    else:
        pp.pprint(stuff)


# NOTE: Might be better off in another library
def peek(name, value):
    """Print a variable's name and value to the console for easy debugging."""

    say("{name}: {value}".format(name, value))
