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
#BUILT_IN_CODE = 'malt-built-in'     # XXX might not need
BACK_CODE = 'malt-back'

# Keyword Sets
HELP_KEYWORDS = ['help', 'options', 'commands']
EXIT_KEYWORDS = ['exit', 'quit', 'abandon']
BACK_KEYWORDS = ['back', 'return', 'done', 'finished']
CLEAR_KEYWORDS = ['clear', 'clean', 'cls']
AFFIRM_KEYWORDS = ["yes", "y", "ok", "sure", "hell yes"]
NEGATE_KEYWORDS = ['no', 'n']


# XXX: no built ins will run when passing empty list
# TODO: split into select() and freeform()
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

    show(PROMPT, nl=False)
    string = _minput().strip().lower()

    if _match(string, options):
        return string
    elif BUILT_IN_FUNCTIONS:
        # Only use built-in funcs if the string has not already been matched.
        # This way the user can override built-ins at their discretion.
        return _match_builtins(string, options)
    else:
        return None


def _match_complex_options(args, prototype):
    """boop"""
    # First assert that the argument list is not empty.
    if len(args) < 1:
        return { 'action': None }

    # If we have a single command, check it against the normal match function.
    elif len(args) == 1:
        act = args[0].strip()
        if _match(act, list(prototype.keys())):
            return { 'action': act }
        elif BUILT_IN_FUNCTIONS:
            return { 'action': _match_builtins(act, list(prototype.keys())) }
        else:
            return { 'action': None }

    # Otherwise enter the complex solution.
    else:
        action = args.pop(0)
        if action not in prototype.keys():
            show('problem')
            return { 'action': None }

        response = { 'action': action }
        # loop through all defined actions until we find the right one
        for cmd, margs in prototype.items():
            if cmd != action:
                continue
            if len(args) != len(list(margs.keys())):
                break
            for name, cast in margs.items():
                try:
                    response[name] = cast(args.pop())
                except ValueError:
                    show('casting error')
                    # should return nothing if one fails
                else:
                    show("cast {} to {}".format(name, str(cast)))

        return response


def freeform(silent=False):
    """Get an unmodified string from the user.

    Input is taken through _minput() so indentation is preserved, and stripped
    of extra whitespace, but otherwise raw.
    """
    if not silent:
        _mprint('[malt] freeform input: ', nl=False)
    return _minput().strip()


def ultra_select(options):
    if not options or type(options) is not list:
        raise ValueError(
            "select requires a list of options (use freeform for raw text)")
    action_key = 'action'
    show(PROMPT, nl=False)
    string = _minput().strip().lower()
    words = [w.strip() for w in string.split()]
    # every argument has to be found and cast to the right type
    argdict = _ultra_parse(options)
    response = _match_complex_options(words, _ultra_parse(options))
    return response



# ex: ['add name val:int', 'remove name']
# TODO: clean up
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


# NOTE: restricted for now to just two arguments
# NOTE: all inputs are set to lowercase; this is not wanted
# XXX: crashes on empty input
# TODO: merge with select
def split_select(options=None, cast=None):
    """Get a command and one arg from the console.
    Optionally cast the argument to a given type.
    """

    # TODO: factor out interfacing code so we can test the logic
    show(PROMPT, nl=False)
    split_string = _minput().strip().split()

    head = split_string[0].strip().lower()
    if len(split_string) > 1:
        tail = split_string[1].strip()
        if cast is not None:
            try:
                tail = cast(tail)
            except ValueError:
                show("[malt] unable to cast {} to {}".format(tail, cast))
                tail = None
    else:
        tail = None

    if _match(head, options):
        return (head, tail)
    else:
        return (_match_builtins(head, options), tail)


def _match(string, options):
    """Evaluate if a string is in a list regardless of case or whitespace."""
    return string.strip().lower() in [o.strip().lower() for o in options]

# TODO: implement multiple option options
#    for opt in options:
#        if type(opt) is list:
#            return string in [o.strip().lower() for o in opt]
#        else:
#            return string == opt.strip().lower()


# TODO: rename
def _match_builtins(string, options):
    """Try to match a given string against built-in convienience functions.

    Called when user input does not match client-given options. These built-in
    functions are for convieniece, so that the client program does not have to
    define them itself. This function will not be called if BUILT_IN_FUNCTIONS
    is disabled.
    """

    if string in HELP_KEYWORDS:
        hint(options)
    elif string in CLEAR_KEYWORDS:
        clear()
    elif string in BACK_KEYWORDS:
        return BACK_CODE
    elif string in EXIT_KEYWORDS:
        if THROW_EXIT_EXCEPTIONS:
            raise SystemExit()
        else:
            return EXIT_CODE
    else:
        show("[malt] unknown keyword")


# NOTE: does not accept normal built-in functions
# NOTE: what happens if high is lower than low?
# TODO: integrate with select
def numeral(low, high, cast=int):
    """Get a number between low and high (inclusive) from the user."""

    show(PROMPT, nl=False)
    number = _minput()
    try:
        number = cast(number)
    except ValueError:
        # could not cast to a number
        return None

    if low <= number and number <= high:
        return number
    else:
        return None


# TODO: implement multiple option options
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
