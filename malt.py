# coding=utf-8

# Malt
# boilerplate for interactive text loops in the console

#import readline  # TODO: improve command history
from subprocess import call

# Default Markings
TITLE_BAR = " ===== Malt ===== "
SHOW_TITLE_BAR = False
PROMPT = "> "
INDENT = ""
LIST_TICK = "-"
PAUSE = "... "

# Select() Codes
EXIT_CODE = 'malt-exit'
BUILT_IN_CODE = 'malt-built-in'
BACK_CODE = 'malt-back'

# Keyword Sets
HELP_KEYWORDS = ['help', 'options', 'commands', 'what', 'ls', 'dir']
EXIT_KEYWORDS = ['exit', 'quit', 'abandon']
BACK_KEYWORDS = ['back', 'return', 'done', 'finished']
CLEAR_KEYWORDS = ['clear', 'clean', 'cls']
AFFIRM_KEYWORDS = [ "yes", "ye", "yeah", "y", "ok", "sure", "why not", 
    "gimme", "hell yes", "heck yes", "do it", "of course", "naturally", 
    "let's go", "yep"
]

# Gen. TODO: integrate colors

class AbandonShip(Exception): pass


def select(options=None):
    """Get one of a limited set of commands from the user.
    Matches are not case-sensitive, and returned strings are always lowercase.
    """

    prompt()
    result = None
    string = input().strip().lower()

    if __matches(string, options):
        return string
    else:
        # Only use built-in functions if the string has not already been matched.
        # This way the user can override built-ins at their discretion.
        return __try_built_ins(string, options)



# NOTE: restricted for now to just two arguments
def split_select(options=None):
    """Get one of a limited set of commands with whitespace-delimited args."""

    prompt()
    split_string = input().strip().lower().split('\w')

    head = split_string[0]
    if len(split_string) > 1:
        tail = split_string[1]
    else:
        tail = None   

    if __matches(head, options):
        return (head, tail)
    else:
        return (__try_built_ins(head, options), tail)


def __matches(string, options):
    """Evaluate if string is in options regardless of case."""

    # Only try to match input if 'options' is a valid list.
    if (type(options) is not list) or (len(options) < 1):
        return True
    # Strings match regardless of case.
    elif string in [o.strip().lower() for o in options]:
        return True
    else:
        return False


# TODO make help message callable
def __try_built_ins(string, options):
    if string in HELP_KEYWORDS:
        hint(options)
        return BUILT_IN_CODE
    elif string in CLEAR_KEYWORDS:
        clear()
        return BUILT_IN_CODE
    elif string in BACK_KEYWORDS:
        return BACK_CODE
    elif string in EXIT_KEYWORDS:
        return EXIT_CODE
    else:
        return None
    

#NOTE: does not accept normal built-in functions
#NOTE: what happens if high is lower than low?
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


def hint(options):
    built_in_options = ['help', 'clear', 'back', 'exit']
    show("[malt] available commands: ", nl='')
    show(options, inline=True)
    show("\nbuilt-in functions ", nl='')
    show(built_in_options, inline=True)
    show(" are available at any time")


# TODO: improve type detection and formatting
# TODO: add support for indenting
# TODO: prevent test from passing 80 chars
def show(stuff, nl='\n', inline=False):
    """Print things to the console.
    Check the type of each object to determine the best printing format.
    """

    stuff_t = type(stuff)
    #print(INDENT, end='')

    # Lists (with both item and sentence form)
    if stuff_t is list:
        # Empty List Marker
        length = len(stuff)
        if length < 1:
            print("[malt] (empty list)")

        # Sentence Style
        if inline:

            # Surround each item with single quotes.
            length = len(stuff)
            qt_stuff = ["'{}'".format(thing) for thing in stuff]

            # Use different formatting for different length lists.
            if length == 1:
                final = "only " + qt_stuff[0]
            elif length == 2:
                final = qt_stuff[0] + " and " + qt_stuff[1]
            elif length >= 3:
                final = ', '.join(qt_stuff[:-1]) + ", and " + qt_stuff[-1]

            print(final, end='')

        # Item Style
        else:
            for thing in stuff:
                print(LIST_TICK, end='')
                print(thing)

    # Dictionaries
    elif stuff_t is dict:
        print("{")
        for (key, value) in stuff.items():
            print("{}:".format(key), end=' ')
            show(value)
        print("}")
    
    # Basics & Exceptions
    else:
        #print("[malt] warning: show does not catch type({})".format(type(stuff)))
        print(stuff, end=nl)


def indent():
    pass


def undent():
    pass


def confirm(silent=False):
    """Ask the user to confirm a yes or no decision using the prompt."""

    if not silent:
        show("[malt] confirm? ", nl='')
    return (input().strip().lower() in AFFIRM_KEYWORDS)


def pause():
    show(PAUSE, nl='')
    input()


def prompt():
    show(PROMPT, nl='')


def clear():
    """Clear the screen. Multiplatform support not yet implemented."""

    call(["clear"])
    if SHOW_TITLE_BAR:
        show(TITLE_BAR)
