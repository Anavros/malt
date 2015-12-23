# coding=utf-8
"""
a collection of tools that make developing interactive text loops easier

...
select() is the most important function in the library. It allows the client
program to specify a list of keyword options for the user to enter. If the user
enters bad input, it is not returned. select() also implements a few common
convienience functions, like printing help messages and clearing the screen.
"""

# TODO:
# import logging
import os
from contextlib import contextmanager

RAISE_SYSTEM_EXIT = True
AUTOCLEAR = False
PREFIX = "[malt] "
MAX_INDENT = 4
INDENT_WIDTH = 2

_indent = 0
_fresh_line = True  # XXX shouldn't be a global (and def not all caps)

OVERFLOW = 80
# constant for height
# Sink depth? rinse depth, soak length?

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
        raise ValueError("A list of options is required.")

    prototype = _parse_options(options)
    allowed_commands = list(prototype.keys())

    if AUTOCLEAR:
        _mprint("="*(OVERFLOW-(_indent*INDENT_WIDTH)))

    words = [w.strip() for w in freefill().split()]

    if AUTOCLEAR:
        rinse()

    if len(words) < 1:
        return Response(None)
    command = words.pop(0).lower()  # NOTE: remaining words are all args

    if _string_included(command, allowed_commands):
        proto_args = prototype[command]
        given_args = words
        need_len = len(proto_args)
        have_len = len(given_args)

        if need_len > have_len:
            serve(PREFIX + "missing arguments")
            return Response(None)
        elif need_len < have_len:
            serve(PREFIX + "too many arguments")
            return Response(None)

        try:
            valid_args = _validate_args(proto_args, given_args)
        except ValueError:
            serve(PREFIX + "invalid argument type")
            return Response(None)
        else:
            return Response(command, valid_args)

    # Only try builtins if the string has not already been matched.
    # XXX: built ins ignore extra arguments
    elif command == 'help':
        _help(options)
        return Response(None)
    elif command == 'clear':
        rinse()
        return Response(None)
    elif command == 'quit':
        if RAISE_SYSTEM_EXIT:
            raise SystemExit()
        else:
            return Response('quit')
    serve(PREFIX + "unknown keyword")
    return Response(None)


def freeform(prompt="> "):
    return freefill(prompt)

def freefill(prompt="> "):
    """Get an unmodified string from the user.

    Input is taken through _minput() so indentation is preserved, and stripped
    of extra whitespace, but otherwise raw.
    """
    serve(prompt, nl=False)
    return _minput().strip()


# XXX Temporary Redirection
def show(stuff='', nl=True):
    return serve(stuff, nl)

def serve(output='', nl=True):
    """Print stuff on the console with smart type formatting.

    Mainly a wrapper around print() to provide extra features that are helpful
    when developing a simple console program. Dispatches lists and dicts into
    hidden helper functions to keep the main declaration short and sweet.

    Optional Arguments:
        -> output (default=''): the data to be printed (type will be detected)
        -> nl (default=True): to print or not to print a newline
    """
    if type(output) in [str, int, float]:
        _mprint(output, nl)

    # NOTE: nested tuples render as str(tuple)
    elif type(output) is tuple:
        if not output:
            _mprint('()')
        else:
            _mprint('(', nl=False)
            for item in output[:-1]:
                _mprint(str(item)+', ', nl=False)
            _mprint(str(output[-1]), nl=False)
            _mprint(')', nl)

    elif type(output) in [list, set, frozenset]:
        _mprint('[', nl=output)
        with indent():
            for i, item in enumerate(output):
                if not _fresh_line:
                    _mprint()
                #_mprint(LIST_TICK, nl=False)
                _mprint("[{}] ".format(i), nl=False)
                serve(item)
        _mprint(']', nl)

    elif type(output) is dict:
        _mprint("{", nl=output)
        with indent():
            for (key, value) in output.items():
                _mprint("{}: ".format(key), nl=False)
                serve(value)
        _mprint("}")

    # Helps with OrderedDict.
    elif hasattr(output, 'items'):
        serve(list(output.items()))

    # Stops objects like str from spewing everywhere.
    elif hasattr(output, '__dict__') and type(output.__dict__) is dict:
    #elif hasattr(output, '__dict__'):
        serve(output.__dict__, nl)

    elif hasattr(output, '_get_args()'):
        serve(list(output._get_args()))

    # When in doubt, use repr.
    else:
        _mprint(repr(output), nl)


@contextmanager
def indent():
    """Increase the global indentation value by one.

    This value is independent of the actual indentation printed to the screen;
    _mprint() handles the number of spaces that are actually printed. Callers
    to indent() do not need to worry about spacing or going over maximum line
    width. Calling malt.indent() is all that is needed.
    """
    global _indent
    _indent = _indent+1
    try:
        yield
    finally:
        _indent = max(_indent-1, 0)


def confirm(prompt=PREFIX + "confirm? "):
    """Receive a yes or no answer from the user.

    Loops until a yes or no has been given. Does not accept unknown input to
    prevent accidental typing errors from causing problems.
    """
    while True:
        serve(prompt, nl=False)
        key = _minput().strip().lower()
        if key == 'yes':
            return True
        elif key == 'no':
            return False
        else:
            serve(PREFIX + "unknown keyword (use 'yes' or 'no')")
            serve()
            continue


# TODO: name needs some thinking
def prepare_stockpile(filename):
    """Set up a log file for malt.stash() to use."""
    pass


def stash(message, level=0):
    """Print a message to a log file."""
    pass


# XXX Temporary Redirection
def pause():
    return savor()

def savor():
    """Pause for dramatic effect.

    Displays a small string defined in PAUSE and waits until the user hits
    enter. Input is not used. Built-in functions are also not available.
    """
    serve(PAUSE, nl=False)
    _minput()


# XXX Temporary Redirection
def clear():
    return rinse()

# debatable whether rinse is better than clear
# if we switch to newlines then yes
def rinse():
    """Clear the screen."""
    if not AUTOCLEAR:
        os.system("cls" if os.name == "nt" else "clear")
    else:
        print('\n'*120)

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


def _mprint(string='', nl=True):
    """Print output to the console with extra functionality.

    Provides support for indentation and line truncation. Every call should go
    through _mprint() as it will ensure indentation will always be correct.
    """
    global _fresh_line, OVERFLOW
    global _indent, MAX_INDENT, INDENT_WIDTH
    already_printed = 0

    # Add indentation to the beginning of every new line.
    if _fresh_line:
        indentation = ' '*min(_indent, MAX_INDENT)*INDENT_WIDTH
        already_printed = len(indentation)
        print(indentation, end='')

    string = str(string)  # cast ints and anything else just to make sure
    end_char = '\n' if nl else ''

    # Wrap the line via recursion if it is too long.
    if already_printed + len(string) > OVERFLOW:
        remaining = OVERFLOW-already_printed
        cut = OVERFLOW  # not 0 to prevent infinite loops on long words
        # should get the whitespace closest to the maximum allowed length
        for i in range(remaining):
            if string[i].isspace():
                cut = i
        print(string[:cut], end='\n')
        _fresh_line = True
        _mprint(string[cut:].strip(), nl)
    else:
        print(string, end=end_char)

    # The next line will be 'fresh' if it follows a newline.
    # NOTE: maybe this *variable* should not be all caps like a constant
    _fresh_line = nl



def _minput():
    """Wrapper for input() to help provide indentation support."""
    global _fresh_line
    _fresh_line = True
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
        serve(PREFIX + "Available Commands:")
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
        raise ValueError(PREFIX + "unknown cast ({})".format(string))
