# coding=utf-8

# Malt
# boilerplate for interactive text loops in the console

import pprint
from subprocess import call
pp = pprint.PrettyPrinter()  # TODO remove eventually

# can be set by the user
TITLE_BAR = " ===== Malt ===== "
SHOW_TITLE_BAR = False
DEFAULT_PROMPT = "> "

# special codes returned from select()
EXIT_CODE = 'malt-exit'
BUILT_IN_CODE = 'malt-built-in'
# BACK_CODE?


# TODO: implement parameters (e.g. "run 4")
def select(options=None):
    """Get one of a limited set of commands from the user.
    Matches are not case-sensitive, and returned strings are always lowercase.
    """

    prompt()
    string = input().strip().lower()

    # do not verify input if no options (or bad options) are given
    # TODO: what about an empty list?
    if type(options) is not list:
        return string

    # match against options regardless of case
    elif string in [o.strip().lower() for o in options]:
        return string

    # only use built-in functions if the string has not already been matched
    # this way the user can override built-ins at their discretion
    elif string in ["help", "options", "commands", "help me", "what", "ls", "dir"]:
        options = ["'{}'".format(o) for o in options]
        if len(options) == 1:
            opt_string = 'only ' + options[0]
        elif len(options) == 2:
            opt_string = options[0] + " and " + options[1]
        elif len(options) > 2:
            opt_string = ', '.join(options[:-1]) + ', and ' + options[-1]

        print("[malt] available commands: {}".format(opt_string))
        print("built-in functions 'help', 'clear', and 'quit' are available at any time")
        return BUILT_IN_CODE

    elif string in ["clear", "clean", "cls", "get this shit out of my face"]:
        clear()
        return BUILT_IN_CODE

    elif string in ["exit", "quit", "abandon ship", "this ship is going down"]:
        return EXIT_CODE

    else:
        return None


# TODO: could be much better
def split_select(options=None):
    """Get a list of multiple arguments split by whitespace from the user.
    Matches are not case-sensitive, and returned strings are always lowercase.
    """

    prompt()
    strings = input().strip().lower().split()
    first = strings[0]

    # do not verify input if no options (or bad options) are given
    # TODO: what about an empty list?
    if type(options) is not list:
        return strings

    # match against options regardless of case
    elif first in [o.strip().lower() for o in options]:
        return strings

    # only use built-in functions if the string has not already been matched
    # this way the user can override built-ins at their discretion
    elif first in ["help", "options", "commands", "help me", "what", "ls", "dir"]:
        options = ["'{}'".format(o) for o in options]
        if len(options) == 1:
            opt_string = 'only ' + options[0]
        elif len(options) == 2:
            opt_string = options[0] + " and " + options[1]
        elif len(options) > 2:
            opt_string = ', '.join(options[:-1]) + ', and ' + options[-1]

        print("[malt] available commands: {}".format(opt_string))
        print("built-in functions 'help', 'clear', and 'quit' are available at any time")
        return BUILT_IN_CODE

    elif first in ["clear", "clean", "cls", "get this shit out of my face"]:
        clear()
        return BUILT_IN_CODE

    elif first in ["exit", "quit", "abandon ship", "this ship is going down"]:
        return EXIT_CODE

    else:
        return None


#NOTE: does not accept normal built-in functions
def numeral(low, high, cast=int):
    """Get a number between low and high (inclusive) from the user."""

    prompt()
    number = input()
    try:
        number = cast(number)
    except ValueError:
        # could not cast to a number
        return None

    if low <= number and number <= high:
        return number
    else:
        return None


# TODO: improve type detection and formatting; remove pprint
def show(stuff):
    """Print things to the console.
    Check the type of each object to determine the best printing format.
    """

    tp = type(stuff)
    if tp is str:
        print(stuff)
    elif tp is list:
        if len(stuff) < 1:
            print("(empty list)")
        else:
            for thing in stuff:
                print("-", end='') # TODO put in var
                print(thing)
    elif isinstance(stuff, object):
        pp.pprint(stuff.__dict__)
    else:
        pp.pprint(stuff)


def confirm(silent=False):
    """Ask the user to confirm a yes or no decision using the prompt."""

    if not silent:
        print("[malt] confirm? ", end='')
    affirmations = [
        "yes", "ye", "yeah", "y", "ok", "sure", "why not", "gimme", "hell yes",
        "heck yes", "do it", "of course", "naturally", "let's go", "yep"
    ]
    return (input().strip().lower() in affirmations)


def prompt():
    print(DEFAULT_PROMPT, end='')


def clear():
    """Clear the screen. Multiplatform support not yet implemented."""

    call(["clear"])
    if SHOW_TITLE_BAR:
        print(TITLE_BAR)
