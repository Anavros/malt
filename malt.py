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

# Indentation Settings
INDENT = 0
MAX_INDENT = 4
INDENT_WIDTH = 4
FRESH_LINE = True
# TODO
MAX_TERM_WIDTH = 80


# Select() Codes
EXIT_CODE = 'malt-exit'
BUILT_IN_CODE = 'malt-built-in'
BACK_CODE = 'malt-back'

# Keyword Sets
HELP_KEYWORDS = ['help', 'options', 'commands', 'what', 'ls', 'dir']
EXIT_KEYWORDS = ['exit', 'quit', 'abandon']
BACK_KEYWORDS = ['back', 'return', 'done', 'finished']
CLEAR_KEYWORDS = ['clear', 'clean', 'cls']
AFFIRM_KEYWORDS = [ "yes", "y", "ok", "sure", "hell yes", "do it", "yep"]


class AbandonShip(Exception): pass


# TODO: allow multiple keywords per option?
def select(options=None):
    """Get one of a limited set of commands from the user.
    Matches are not case-sensitive, and returned strings are always lowercase.
    """

    prompt()
    result = None
    string = __minput().strip().lower()

    if __matches(string, options):
        return string
    else:
        # Only use built-in functions if the string has not already been matched.
        # This way the user can override built-ins at their discretion.
        return __try_built_ins(string, options)



# NOTE: restricted for now to just two arguments
def split_select(options=None, cast=None):
    """Get a command and one arg from the console.
    Optionally cast the argument to a given type.
    """

    prompt()
    split_string = __minput().strip().lower().split()
    #print("string = {}".format(split_string))

    head = split_string[0].strip()
    if len(split_string) > 1:
        tail = split_string[1].strip()
        if cast is not None:
            try: tail = cast(tail)
            except ValueError:
                show("[malt] unable to cast {} to {}".format(tail, cast))
                tail = None
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
# TODO: document and clean up
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
    number = __minput()
    try:
        number = cast(number)
    except ValueError:
        # could not cast to a number
        return None

    if low <= number and number <= high:
        return number
    else:
        return None


# Gen. TODO: integrate colors
# NOTE: should we let programs use colors?
def enable_colors():
    pass


def hint(options):
    built_in_options = ['help', 'clear', 'back', 'exit']
    show("[malt] available commands: ", nl='')
    show(options, inline=True)
    show("")
    show("built-in functions ", nl='')
    show(built_in_options, inline=True)
    show(" are available at any time")


# TODO: prevent test from passing 80 chars
# TODO: add color support
# TODO: improve unknown item support
# TODO: print a newline if no args are given
def show(stuff, nl='\n', inline=False):
    """Print things to the console.
    Check the type of each object to determine the best printing format.
    """
    stuff_t = type(stuff)

    # Lists (with both item and sentence form)
    if stuff_t is list:
        # Empty List Marker
        length = len(stuff)
        if length < 1:
            __mprint("[malt] (empty list)")

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

            __mprint(final, nl='')

        # Item Style
        else:
            for thing in stuff:
                __mprint(LIST_TICK, nl='')
                __mprint(thing)

    # Dictionaries
    elif stuff_t is dict:
        __mprint("{")
        for (key, value) in stuff.items():
            __mprint("{}:".format(key), nl=' ')
            show(value)
        __mprint("}")

    # Basics & Exceptions
    else:
        #print("[malt] warning: show does not catch type({})".format(type(stuff)))
        __mprint(stuff, nl=nl)


def __mprint(string, nl='\n'):
    """Print a string to the console with indentation only if the string is on
    a new line. Wrapper around print() to provide indentation functionality.
    """
    global FRESH_LINE
    if FRESH_LINE:
        indentation = ' '*INDENT*INDENT_WIDTH
        print(indentation, end='')
    print(string, end=nl)
    FRESH_LINE = ('\n' in nl)


def __minput():
    global FRESH_LINE
    FRESH_LINE = True
    return input()


def indent():
    global INDENT
    INDENT = min(INDENT+1, MAX_INDENT)


def undent():
    global INDENT
    INDENT = max(INDENT-1, 0)


def confirm(silent=False):
    """Ask the user to confirm a yes or no decision using the prompt."""

    if not silent:
        show("[malt] confirm? ", nl='')
    return (__minput().strip().lower() in AFFIRM_KEYWORDS)


def pause():
    show(PAUSE, nl='')
    __minput()


def prompt():
    show(PROMPT, nl='')


def clear():
    """Clear the screen. Multiplatform support not yet implemented."""

    call(["clear"])
    if SHOW_TITLE_BAR:
        show(TITLE_BAR)
