# coding=utf-8

# Malt
# boilerplate for interactive text loops in the console

#import readline  # TODO: improve command history
from time import sleep
from subprocess import call

#TODO: separate show function/option to set level of importance
# so you can set a debug flag to mask level x and below
# or, you know, proper logging

SHOW_TITLE_BAR = False
THROW_EXIT_EXCEPTIONS = True
BUILT_IN_FUNCTIONS = True

# Default Markings
TITLE_BAR = " ===== Malt ===== "
PROMPT = "> "
INDENT = ""
LIST_TICK = "-"
PAUSE = "... "

# Indentation Settings
INDENT = 0
MAX_INDENT = 4
INDENT_WIDTH = 2
FRESH_LINE = True
# TODO
MAX_TERM_WIDTH = 80


# Select() Codes
EXIT_CODE = 'malt-exit'
BUILT_IN_CODE = 'malt-built-in'
BACK_CODE = 'malt-back'

# Keyword Sets
HELP_KEYWORDS = ['help', 'options', 'commands']
EXIT_KEYWORDS = ['exit', 'quit', 'abandon']
BACK_KEYWORDS = ['back', 'return', 'done', 'finished']
CLEAR_KEYWORDS = ['clear', 'clean', 'cls']
AFFIRM_KEYWORDS = ["yes", "y", "ok", "sure", "hell yes"]
NEGATE_KEYWORDS = ['no', 'n']


class AbandonShip(Exception): 
    pass


# TODO: allow multiple keywords per option?
# XXX: no built ins will run when passing empty list
# TODO: consider adding "unknown command" line here
def select(options=None):
    """Get one of a limited set of commands from the user.
    Matches are not case-sensitive, and returned strings are always lowercase.
    """

    prompt()
    result = None
    string = __minput().strip().lower()

    if __matches(string, options):
        return string
    elif BUILT_IN_FUNCTIONS:
        # Only use built-in functions if the string has not already been matched.
        # This way the user can override built-ins at their discretion.
        return __try_built_ins(string, options)
    else:
        return None



# NOTE: restricted for now to just two arguments
# NOTE: all inputs are set to lowercase; this is not wanted
# XXX: crashes on empty input
def split_select(options=None, cast=None):
    """Get a command and one arg from the console.
    Optionally cast the argument to a given type.
    """

    prompt()
    split_string = __minput().strip().split()

    head = split_string[0].strip().lower()
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

# TODO: implement multiple option options
#    for opt in options:
#        if type(opt) is list:
#            return string in [o.strip().lower() for o in opt]
#        else:
#            return string == opt.strip().lower()


# TODO make help message callable
# TODO: document and clean up
def __try_built_ins(string, options):
    """Try to match a given string against built-in convienience functions."""
    if string in HELP_KEYWORDS:
        hint(options)
        return BUILT_IN_CODE
    elif string in CLEAR_KEYWORDS:
        clear()
        return BUILT_IN_CODE
    elif string in BACK_KEYWORDS:
        return BACK_CODE
    elif string in EXIT_KEYWORDS:
        if THROW_EXIT_EXCEPTIONS:
            raise AbandonShip()
        else:
            return EXIT_CODE
    else:
        show("[malt] unknown keyword")
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


# TODO: implement multiple option options
def hint(options):
    built_in_options = ['help', 'clear', 'back', 'exit']
    show("[malt] available commands: ", nl=False)
    show(options, inline=True)
    show("")
    show("built-in functions ", nl=False)
    show(built_in_options, inline=True)
    show(" are available at any time")


# TODO: add color support
# TODO: prevent output from passing 80 chars
def show(stuff='', nl=True, slow=0):
    """Print things to the console.
    Check the type of each object to determine the best printing format.
    """
    stuff_t = type(stuff)
    if stuff_t is list or stuff_t is set:
        __show_list(stuff, nl, slow)
    elif stuff_t is dict:
        __show_dict(stuff, nl, slow)
    elif hasattr(stuff, '__dict__'):
        show(stuff.__dict__)
    else:
        __mprint(stuff, nl, slow)


def __show_list(stuff, nl, slow):
    """Display a list as a series of newline-separated ticks."""
    length = len(stuff)
    if length < 1:
        __mprint("(empty list)")

    # Item Style
    else:
        indent()
        for thing in stuff:
            __ensure_newline()
            __mprint(LIST_TICK, nl=False)
            __mprint(thing)
            sleep(slow)
        undent()
    

def __show_dict(stuff, nl, slow, inline):
    """Display dictionaries as key: value pairs where every value is fed back
    through show() recursively to recieve the right formatting.
    """
    __mprint("{")
    indent()
    for (key, value) in stuff.items():
        __mprint("{}: ".format(key), nl=False)
        show(value)
        sleep(slow)
    undent()
    __mprint("}")


def __mprint(string='', nl=True, slow=0):
    """Print output to the console with extra functionality.
    Provides support for indentation and slowed printing.
    """
    global FRESH_LINE
    if FRESH_LINE:
        indentation = ' '*min(INDENT, MAX_INDENT)*INDENT_WIDTH
        print(indentation, end='')
    end_char = '\n' if nl else ''

    if slow > 0:
        for char in string:
            print(char)
            sleep(slow)
        print('', end=end_char, flush=True)
    else:
        print(string, end=end_char)
    FRESH_LINE = nl


def __minput():
    """Wrapper for input() to help provide indentation support."""
    global FRESH_LINE
    FRESH_LINE = True
    return input()


def __ensure_newline():
    if not FRESH_LINE:
        __mprint()


def english(stuff):
    """Compile a list into a string where every element is wrapped in single
    quotes and written out in sentence form.
    """
    if type(stuff) is list:
        length = len(stuff)
        qt_stuff = ["'{}'".format(thing) for thing in stuff]

        # Use different formatting for different length lists.
        if length == 1:
            final = "only " + qt_stuff[0]
        elif length == 2:
            final = qt_stuff[0] + " and " + qt_stuff[1]
        elif length >= 3:
            final = ', '.join(qt_stuff[:-1]) + ", and " + qt_stuff[-1]
        return final
    else:
        __mprint("[malt] can not english-ify a non list")
        return stuff


def indent():
    global INDENT
    INDENT = INDENT+1


def undent():
    global INDENT
    INDENT = max(INDENT-1, 0)


def confirm(silent=False):
    """Ask the user to confirm a yes or no decision using the prompt."""
    while True:
        if not silent:
            show("[malt] confirm? ", nl=False)
        key = __minput().strip().lower()
        if key in AFFIRM_KEYWORDS:
            return True
        elif key in NEGATE_KEYWORDS:
            return False
        else:
            show("[malt] unknown keyword")
            show()
            continue


def pause():
    show(PAUSE, nl=False)
    __minput()


def prompt():
    show(PROMPT, nl=False)


def clear():
    """Clear the screen. Multiplatform support not yet implemented."""

    call(["clear"])
    if SHOW_TITLE_BAR:
        show(TITLE_BAR)
