# coding=utf-8

# Malt
# boilerplate for interactive text loops in the console

import pprint
from subprocess import call
pp = pprint.PrettyPrinter()

MALT_CLEAR_BEFORE_PROMPT = False
MALT_SHOW_TITLE_BAR = False

malt_title_string = " ===== Malt ===== "

def limited_input(options):
    """Get one of a limited set of commands from the user.
    Commands are not case-sensitive.
    Raise ValueError if the user gives mismatched input; it is up to the caller
    to handle the exception and move forward.
    """
    
    if (type(options) is not list) or (len(options) < 1):
        raise TypeError("Options must be a list!")
    
    string = input()
    # check regardless of case or excess whitespace
    if string.strip().lower() in [x.strip().lower() for x in options]:
        return string
    else:
        raise ValueError("User did not give a valid option.")


# Tested
def numeral_input(lower, upper):
    """Get a number between lower and upper from the console."""

    try:
        number = int(input())
    except ValueError:
        raise TypeError("User did not give a useful number.")

    if lower < number and number < upper:
        return number
    else:
        raise ValueError("Given number does not fall within bounds.")


def confirm(string):
    """Ask the user to confirm a yes or no decision using the prompt."""


def say(stuff):
    """Print things to the console.
    Check the type of each object to determine the best printing format.
    """

    if type(stuff) is str:
        print(stuff)
    elif isinstance(stuff, object):
        pp.pprint(stuff.__dict__)
    else:
        pp.pprint(stuff)


def show_help(options):
    print("Malt: available commands are {}".format(options))


def show_bad_input():
    print("Malt: unknown command")
    print("Malt: enter 'help' for a list of available commands")


def prompt(token="> "):
    if MALT_CLEAR_BEFORE_PROMPT:
        clear()
    if MALT_SHOW_TITLE_BAR: # BONUS: use colors 
        print()
        print(malt_title_string)

    print(token, end='')


def pause(token=" --- "):
    print(token)
    input()


# NOTE: Might be better off in another library
def peek(name, value):
    """Print a variable's name and value to the console for easy debugging."""

    say("{name}: {value}".format(name, value))


def clear():
    """Clear the screen."""
    call(["clear"])
