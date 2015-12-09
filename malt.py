# coding=utf-8
"""
a collection of tools that make developing interactive text loops easier

...
select() is the most important function in the library. It allows the client
program to specify a list of keyword options for the user to enter. If the user
enters bad input, it is not returned. select() also implements a few common
convienience functions, like printing help messages and clearing the screen.
"""

# import readline  # TODO: improve command history
from time import sleep
from subprocess import call
from collections import OrderedDict

# TODO: separate show function/option to set level of importance
# so you can set a debug flag to mask level x and below
# or, you know, proper logging

# Global Options
SHOW_TITLE_BAR = False          # NOTE
THROW_EXIT_EXCEPTIONS = True    # raise SystemExit on exit keyword
BUILT_IN_FUNCTIONS = True       # use built-in funcs if input does not match

# Default Markings
# These can be set by the client program if desired.
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
MAX_TERM_WIDTH = 80  # TODO


# Select() Codes
# These codes are returned from the select() function if the user triggers a
# built-in function like 'exit' or 'clear'. If THROW_EXIT_EXCEPTIONS is true,
# the exit function will raise SystemExit instead of returning EXIT_CODE.
# All built-in functionality is disabled if BUILT_IN_FUNCTIONS is False.
EXIT_CODE = 'malt-exit'
BACK_CODE = 'malt-back'

# Keyword Sets
HELP_KEYWORDS = ['help', 'options', 'commands']
EXIT_KEYWORDS = ['exit', 'quit', 'abandon']
BACK_KEYWORDS = ['back', 'return', 'done', 'finished']
CLEAR_KEYWORDS = ['clear', 'clean', 'cls']
AFFIRM_KEYWORDS = ["yes", "y", "ok", "sure", "hell yes"]
NEGATE_KEYWORDS = ['no', 'n']


# could create prototype automatically?
# what if the return was a complex object, where if you tried to match it
# directly, it would just return the right thing?
def select(options):
    """Take user input and return it only if it matches a given set of options.

    If input is not in options, return None instead. This makes the return
    value much easier to check in the client program. If BUILT_IN_FUNCTIONS is
    enabled, run the input past internal convienience functions after checking
    against the main options. If it matches an internal function, run that
    instead.

    If the client passes in an option that is identical to a built-in keyword,
    the associated built-in function will NOT run, and the keyword will be
    returned as normal. This allows the client to overwrite built-ins at will.

    Matches are not case-sensitive, and returned strings are always lowercase.

    Required Arguments:
        -> options: only return input if included in this list of strings
    """

    if not options or type(options) is not list:
        raise ValueError(
            "select requires a list of options (use freeform for raw text)")

    string = _prompt()
    if _string_in_options(string, options):
        return string.lower()

    # Only try builtins if the string has not already been matched.
    elif BUILT_IN_FUNCTIONS and _string_in_builtins(string):
        if string in EXIT_KEYWORDS:
            if THROW_EXIT_EXCEPTIONS:
                raise SystemExit()
            else:
                return EXIT_CODE
        elif string in BACK_KEYWORDS:
            return BACK_CODE
        elif string in HELP_KEYWORDS:
            hint(options)
        elif string in CLEAR_KEYWORDS:
            clear()
    else:
        show("[malt] unknown keyword")
        return None


def _prompt():
    show(PROMPT, nl=False)
    return _minput().strip()


def _string_in_options(string, options):
    """Evaluate if a string is in a list regardless of case or whitespace."""
    return string.strip().lower() in [o.strip().lower() for o in options]


def _string_in_builtins(string):
    """Evaluate if a string is in any list of accepted built-in keywords."""
    return _string_in_options(string,
        HELP_KEYWORDS+CLEAR_KEYWORDS+BACK_KEYWORDS+EXIT_KEYWORDS)


# NOTE: the name is still up for tweaking
def complex_select(options):

    # XXX: what happens if given a list of numbers?
    empty_response = { 'action': None }
    string = prompt()

    prototype = _ultra_parse(options)
    options = list(prototype.keys())

    words = [w.strip() for w in string.split()]
    head = words[0]
    tail = words[1:]

    if _string_in_options(head, options):
        if _verify_arguments(tail, prototype):
            argvalues = get_args(words, prototype)
            response = { k:v for k, v in argvalues.items() }
            response['action'] = head
        else:
            response = empty_response

        return response

    elif BUILT_IN_FUNCTIONS and _string_in_builtins(head, options):
        if string in EXIT_KEYWORDS:
            if THROW_EXIT_EXCEPTIONS:
                raise SystemExit()
            else:
                return EXIT_CODE
        elif string in BACK_KEYWORDS:
            return BACK_CODE
        elif string in HELP_KEYWORDS:
            hint(options)
        elif string in CLEAR_KEYWORDS:
            clear()
    else:
        show("[malt] unknown keyword")
        return empty_response


# TODO: clean up
# ex: ['add name val:int', 'remove name']
def _ultra_parse(arguments):
    struct = OrderedDict()
    # for option?
    for arg in arguments:
        # ex: 'add name val:int'
        argparts = arg.strip().lower().split()
        action = argparts.pop(0)
        if ':' in action:
            raise ValueError("option badly formatted (do not type first arg)")

        struct[action] = {}
        for part in argparts:
            # ex: 'val:int'
            part = part.strip()
            pieces = part.split(':')
            if len(pieces) == 1:
                (part_name, part_type) = (part, 'str')
            elif len(pieces) == 2:
                (part_name, part_type) = part.split(':')
            else:
                raise ValueError("option badly formatted (name or name:type)")

            struct[action][part_name] = part_type

    #show(struct)
    return _replace_casts(struct)


def _replace_casts(argdict):
    for (action, args) in argdict.items():
        argdict[action] = { n:_string_to_type(s) for n, s in args.items() }
    return argdict


def _string_to_type(string):
    if string == 'str':
        return str
    elif string == 'int':
        return int
    elif string == 'float':
        return float
    elif string == 'bool':
        return bool
    else:
        raise ValueError("[malt] unknown cast ({})".format(string))


# combine with prompt
def freeform(silent=False):
    """Get an unmodified string from the user.

    Input is taken through _minput() so indentation is preserved, and stripped
    of extra whitespace, but otherwise raw.
    """
    if not silent:
        _mprint('[malt] freeform input: ', nl=False)
    return _minput().strip()





### DISPLAY FUNCTIONS ###
#########################

def hint(options=None):
    """Display a help message, optionally with a list of allowed commands."""

    if options:
        show("[malt] available commands: {}".format(english(options)))

    bifs = english(['help', 'clear', 'back', 'exit'])
    show("[malt] built-in functions {} are available at any time".format(bifs))


# TODO: add color support
# TODO: prevent output from passing 80 chars
# TODO: allow multiple args like print()
# TODO: add special display for empty string
# NOTE: messes up on OrderedDict
def show(stuff='', nl=True, slow=0):
    """Print stuff on the console with smart type formatting.

    Mainly a wrapper around print() to provide extra features that are helpful
    when developing a simple console program. Dispatches lists and dicts into
    hidden helper functions to keep the main declaration short and sweet.

    Optional Arguments:
        -> stuff (default=''): the data to be printed (type will be detected)
        -> nl (default=True): to print or not to print a newline
        -> slow (default=0): the delay in seconds between printing chars
    """

    stuff_t = type(stuff)
    if stuff_t is list or stuff_t is set:
        _show_list(stuff, nl, slow)
    elif stuff_t is dict:
        _show_dict(stuff, nl, slow)
    elif hasattr(stuff, '__dict__'):
        show(stuff.__dict__)
    else:
        _mprint(stuff, nl, slow)


def _show_list(stuff, nl, slow):
    """Display a list as a series of newline-separated ticks."""
    length = len(stuff)
    if length < 1:
        _mprint("(empty list)")

    # Item Style
    else:
        indent()
        for thing in stuff:
            _ensure_newline()
            _mprint(LIST_TICK, nl=False)
            _mprint(thing)
            sleep(slow)
        undent()


def _show_dict(stuff, nl, slow):
    """Display dictionaries as key: value pairs.

    Every value is fed back through show() recursively to recieve the right
    formatting regardless of type.
    """

    _mprint("{")
    indent()
    for (key, value) in stuff.items():
        _mprint("{}: ".format(key), nl=False)
        show(value)
        sleep(slow)
    undent()
    _mprint("}")


def _mprint(string='', nl=True, slow=0):
    """Print output to the console with extra functionality.

    Provides support for indentation and slowed printing. Every call should go
    through _mprint() as it will ensure indentation will always be correct.
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


def _minput():
    """Wrapper for input() to help provide indentation support."""
    global FRESH_LINE
    FRESH_LINE = True
    return input()


def _ensure_newline():
    if not FRESH_LINE:
        _mprint()


def english(stuff):
    """Compile a list into a string where every element is wrapped in single
    quotes and written out in sentence form.

    Example:
        english(['spam', 'spam', 'eggs']) -> \"'spam', 'spam', and 'eggs'\"
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
        _mprint("[malt] can not english-ify a non list")
        return stuff


def indent():
    """Increase the global indentation value by one.

    This value is independent of the actual indentation printed to the screen;
    _mprint() handles the number of spaces that are actually printed. Callers
    to indent() do not need to worry about spacing or going over maximum line
    width. Calling malt.indent() is all that is needed.
    """
    global INDENT
    INDENT = INDENT+1


def undent():
    """Decrease the global indentation value by one.

    Like indent(), the value is independent of actual characters printed to
    the screen. Guards against lower-than-zero indentation.
    """
    global INDENT
    INDENT = max(INDENT-1, 0)


def confirm(silent=False):
    """Receive a yes or no answer from the user.

    Loops until a yes or no has been given. Does not accept unknown input to
    prevent accidental typing errors from causing problems. If silent,
    confirm() does not print its prompt.
    """
    while True:
        if not silent:
            show("[malt] confirm? ", nl=False)
        key = _minput().strip().lower()
        if key in AFFIRM_KEYWORDS:
            return True
        elif key in NEGATE_KEYWORDS:
            return False
        else:
            show("[malt] unknown keyword")
            show()
            continue


def pause():
    """Pause for dramatic effect.

    Displays a small string defined in PAUSE and waits until the user hits
    enter. Input is not used. Built-in functions are also not available.
    """
    show(PAUSE, nl=False)
    _minput()


# TODO: consider removing title bar
def clear():
    """Clear the screen.

    Multiplatform support not yet implemented. If SHOW_TITLE_BAR is enabled,
    print the title bar defined in TITLE_BAR as the first thing on the fresh
    screen.
    """

    call(["clear"])
    if SHOW_TITLE_BAR:
        show(TITLE_BAR)
