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

EXIT_CODE = 'malt-exit'
BUILT_IN_CODE = 'malt-built-in'


# TODO: integrate decorations
def select(options=None):
    """Get one of a limited set of commands from the user.
    Matches are not case-sensitive, and returned strings are always lowercase.
    """

    prompt()
    string = input().strip().lower()

    if type(options) is not list:
        return string
    elif string in [o.strip().lower() for o in options]:
        return string

    # only use built-in functions if the string has not already been matched
    # this way the user can override built-ins at their discretion
    elif string in ["help", "options", "commands", "help me", "what"]:
        opt_string = ', '.join(options) # TODO: fancify
        print("malt: available commands are {}".format(opt_string))
        print("malt: built-in commands help and clear are also available at any time.")
        return BUILT_IN_CODE

    elif string in ["clear", "clean", "cls", "get this shit out of my face"]:
        clear()
        return BUILT_IN_CODE

    elif string in ["exit", "quit", "abandon ship"]:
        return EXIT_CODE

    else:
        return None


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


def show(stuff):
    """Print things to the console.
    Check the type of each object to determine the best printing format.
    """

    if type(stuff) is str:
        print(stuff)
    elif isinstance(stuff, object):
        pp.pprint(stuff.__dict__)
    else:
        pp.pprint(stuff)


def confirm(silent=False):
    """Ask the user to confirm a yes or no decision using the prompt."""

    if not silent:
        print("malt: confirm? ", end='')
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
