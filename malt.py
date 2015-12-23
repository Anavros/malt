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
from subprocess import call
from contextlib import contextmanager

# TODO: separate show function/option to set level of importance
# so you can set a debug flag to mask level x and below
# or, you know, proper logging

# Global Options
THROW_EXIT_EXCEPTIONS = True    # raise SystemExit on exit keyword
BUILT_IN_FUNCTIONS = True       # use built-in funcs if input does not match

# Default Markings
# These can be set by the client program if desired.
PROMPT = "> "
INDENT = ""
LIST_TICK = "-"
PAUSE = "... "

# Indentation Settings
INDENT = 0
MAX_INDENT = 4
INDENT_WIDTH = 2
MAX_LINE_WIDTH = 80  # overflow
FRESH_LINE = True  # XXX shouldn't be a global (and def not all caps)

# Select() Codes  # XXX consider removing
EXIT_CODE = 'malt-exit'
BACK_CODE = 'malt-back'

# Keyword Sets XXX consider reducing to one keyword each
HELP_KEYWORDS = ['help', 'options', 'commands']
EXIT_KEYWORDS = ['exit', 'quit', 'abandon']
BACK_KEYWORDS = ['back', 'return', 'done', 'finished']
CLEAR_KEYWORDS = ['clear', 'clean', 'cls']
AFFIRM_KEYWORDS = ["yes", "y", "ok", "sure", "hell yes"]
NEGATE_KEYWORDS = ['no', 'n']

# NOTE: Theme Words:
# response, answer, extract, fill, supply, satisfy, overflow, flow, pour,
# glass, provide, dispense, serve,

# XXX Temporary Redirection
def select(options):
    return fill(options)


def fill(options):
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
            "select requires a list of options (use freeform() for raw text)")

    prototype = _parse_options(options)
    allowed_commands = list(prototype.keys())

    words = [w.strip() for w in freeform().split()]
    if len(words) < 1:
        return Response(None)
    command = words.pop(0).lower()  # NOTE: remaining words are all args

    if _string_included(command, allowed_commands):
        proto_args = prototype[command]
        given_args = words
        need_len = len(proto_args)
        have_len = len(given_args)

        if need_len > have_len:
            show("[malt] missing arguments")
            return Response(None)
        elif need_len < have_len:
            show("[malt] too many arguments")
            return Response(None)

        try:
            valid_args = _validate_args(proto_args, given_args)
        except ValueError:
            show("[malt] invalid argument type")
            return Response(None)
        else:
            return Response(command, valid_args)

    # Only try builtins if the string has not already been matched.
    # XXX: built ins ignore extra arguments
    elif BUILT_IN_FUNCTIONS:
        if command in EXIT_KEYWORDS:
            if THROW_EXIT_EXCEPTIONS:
                raise SystemExit()
            else:
                return Response(EXIT_CODE)
        elif command in BACK_KEYWORDS:
            return Response(BACK_CODE)
        elif command in HELP_KEYWORDS:
            _help(options)
            return Response(None)
        elif command in CLEAR_KEYWORDS:
            clear()
            return Response(None)
    show("[malt] unknown keyword")
    return Response(None)


def freeform(prompt=PROMPT):
    return freefill(prompt)

def freefill(prompt="> "):
    """Get an unmodified string from the user.

    Input is taken through _minput() so indentation is preserved, and stripped
    of extra whitespace, but otherwise raw.
    """
    show(prompt, nl=False)
    return _minput().strip()


# XXX Temporary Redirection
def show(stuff='', nl=True):
    return serve(stuff, nl)

# TODO: add color support
# NOTE: messes up on OrderedDict
def serve(output='', nl=True):
    """Print stuff on the console with smart type formatting.

    Mainly a wrapper around print() to provide extra features that are helpful
    when developing a simple console program. Dispatches lists and dicts into
    hidden helper functions to keep the main declaration short and sweet.

    Optional Arguments:
        -> stuff (default=''): the data to be printed (type will be detected)
        -> nl (default=True): to print or not to print a newline
    """

    cast = type(output)
    if cast in [list, set, frozenset]:
        _show_list(output, nl)
    elif cast is dict:
        _show_dict(output, nl)
    elif hasattr(output, '__dict__'):
        serve(output.__dict__)
    elif cast in [str, int, float, bin, oct]:
        _mprint(output, nl)
    else:
        serve("[malt] unhandled serve type")
        print(output, nl)


@contextmanager
def indent():
    """Increase the global indentation value by one.

    This value is independent of the actual indentation printed to the screen;
    _mprint() handles the number of spaces that are actually printed. Callers
    to indent() do not need to worry about spacing or going over maximum line
    width. Calling malt.indent() is all that is needed.
    """
    global INDENT
    INDENT = INDENT+1
    try:
        yield
    finally:
        INDENT = max(INDENT-1, 0)


def confirm(prompt="[malt] confirm? "):
    """Receive a yes or no answer from the user.

    Loops until a yes or no has been given. Does not accept unknown input to
    prevent accidental typing errors from causing problems.
    """
    while True:
        show(prompt, nl=False)
        key = _minput().strip().lower()
        if key in AFFIRM_KEYWORDS:
            return True
        elif key in NEGATE_KEYWORDS:
            return False
        else:
            show("[malt] unknown keyword")
            show()
            continue


# XXX Temporary Redirection
def pause():
    return savor()

def savor():
    """Pause for dramatic effect.

    Displays a small string defined in PAUSE and waits until the user hits
    enter. Input is not used. Built-in functions are also not available.
    """
    show(PAUSE, nl=False)
    _minput()


# XXX Temporary Redirection
def clear():
    return rinse()

def rinse():
    """Clear the screen.

    Multiplatform support not yet implemented.
    os.system('cls if os.something=='nt' etc etc)
    """

    call(["clear"])

### INTERNAL UTILITIES ### These should have their own module but I want
########################## to fit malt into a single file!

# ideas: glass, brew
class Response(object):
    """..."""
    def __init__(self, command=None, args=None):
        self.command = command
        if args is not None:
            for (key, value) in args:
                self.__dict__[key] = value

    def __eq__(self, string):
        return string == self.command


def _show_list(stuff, nl):
    """Display a list as a series of newline-separated ticks."""

    if len(stuff) < 1:
        _mprint("(empty list)")
        return

    with indent():
        for thing in stuff:
            if not FRESH_LINE:
                _mprint()
            _mprint(LIST_TICK, nl=False)
            _mprint(thing)


def _show_dict(stuff, nl):
    """Display dictionaries as key: value pairs.

    Every value is fed back through show() recursively to recieve the right
    formatting regardless of type.
    """
    if len(stuff.items()) < 1:
        _mprint("(empty dict)")
        return

    _mprint("{")
    with indent():
        for (key, value) in stuff.items():
            _mprint("{0}: ".format(key), nl=False)
            show(value)
    _mprint("}")


def _mprint(string='', nl=True):
    """Print output to the console with extra functionality.

    Provides support for indentation and line truncation. Every call should go
    through _mprint() as it will ensure indentation will always be correct.
    """
    global FRESH_LINE, MAX_LINE_WIDTH
    global INDENT, MAX_INDENT, INDENT_WIDTH
    already_printed = 0

    # Add indentation to the beginning of every new line.
    if FRESH_LINE:
        indentation = ' '*min(INDENT, MAX_INDENT)*INDENT_WIDTH
        already_printed = len(indentation)
        print(indentation, end='')

    string = str(string)  # cast ints and anything else just to make sure
    end_char = '\n' if nl else ''

    # Wrap the line via recursion if it is too long.
    if already_printed + len(string) > MAX_LINE_WIDTH:
        remaining = MAX_LINE_WIDTH-already_printed
        cut = MAX_LINE_WIDTH  # not 0 to prevent infinite loops on long words
        # should get the whitespace closest to the maximum allowed length
        for i in range(remaining):
            if string[i].isspace():
                cut = i
        print(string[:cut], end='\n')
        FRESH_LINE = True
        _mprint(string[cut:].strip(), nl)
    else:
        print(string, end=end_char)

    # The next line will be 'fresh' if it follows a newline.
    # NOTE: maybe this *variable* should not be all caps like a constant
    FRESH_LINE = nl



def _minput():
    """Wrapper for input() to help provide indentation support."""
    global FRESH_LINE
    FRESH_LINE = True
    return input()


def _string_included(string, options):
    """Evaluate if a string is in a list regardless of case or whitespace."""
    return string.strip().lower() in [o.strip().lower() for o in options]


def _validate_args(proto, given):
    # we're assuming the two lists are lined up in the correct order
    return [(name, cast(given.pop(0))) for name, cast in proto]


# TODO: refactor with parsing functions
def _help(options):
    with indent():
        show("[malt] Available Commands:")
        for string in options:
            words = string.split()
            command = words.pop(0)
            _mprint("- {} ".format(command), nl=False)
            for arg in words:
                parts = arg.split(':')
                if len(parts) == 2:
                    name = parts[0]
                    cast = parts[1]
                elif len(parts) == 1:
                    name = parts[0]
                    cast = 'str'
                _mprint("[{} {}]".format(cast, name), nl=False)
            _mprint()


def _parse_options(option_list):
    prototype = {}
    for option in option_list:
        words = option.strip().lower().split()
        command = words.pop(0)
        if ':' in command:
            raise ValueError("option badly formatted (do not type first arg)")

        prototype[command] = _parse_arg_list(words)
    return _replace_casts(prototype)


def _parse_arg_list(words):
    proto_args = []
    for word in words:
        if len(word.split(':')) == 1:
            word = word + ':str'
        proto_args.append(word.split(':'))
    return proto_args


def _replace_casts(argdict):
    for (action, args) in argdict.items():
        argdict[action] = [ (n, _string_to_type(s)) for n, s in args ]
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
