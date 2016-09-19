
import re
import malt.parse as parse
from malt.exceptions import *

try:
    import readline
except ImportError:
    pass

"""Malt
A tiny toolkit for structured input and output.
"""


def offer(options):
    """Offer the user a list of options. Input is verified as returned as a
    Response object."""
    #maybe give a warning if the user tries something like `bad o():arg`
    #which would never match anything
    syntax = parse.parse(options)

    try:
        raw_text = input('> ')
    except (KeyboardInterrupt, EOFError):
        # Design point: Allow option to not exit immediately?
        # Put special variable in response and allow user?
        # Possibly extensible options where user can define built-in funcs?
        raise SystemExit  # silent

    try:
        head, args, kwargs = parse.parse_response(raw_text)
    except (EmptyCommand, InputForbiddenCharacters) as e:
        empty = type(e) is EmptyCommand
        return Response(valid=False, error=e, empty=empty)

    try:
        syn = syntax[head]
    except KeyError:
        return Response(head=head, raw_args=args, raw_kwargs=kwargs,
            valid=False, error=UnknownCommand())

    try:
        body = parse.validate((args, kwargs), syn)
    except (WrongType, NotAnOption, TooManyArgs, NotEnoughArgs) as e:
        return Response(head, raw_args=args, raw_kwargs=kwargs,
            valid=False, error=e)
    return Response(head, body, raw_args=args, raw_kwargs=kwargs, valid=True)


# TODO: allow loading list of strings
def load(filepath, options=None):
    """
    Load a list of responses from a file. Each line is processed in the same way
    as input from stdin. If options are not given, `load` will search for syntax
    hints, lines starting with '?' and describing one option, in the file.
    """
    if options:
        syntax = parse.parse(options)
    else:
        syntax = parse.parse(parse.syntax_hints(filepath))
    responses = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.split('#')[0].strip()
            line = line.split('?')[0].strip()
            if not line: continue

            head, raw_args, raw_kwargs = parse.parse_response(line)
            body = parse.validate((raw_args, raw_kwargs), syntax[head])
            responses.append(Response(head, body, raw_args, raw_kwargs, valid=True))
    return responses


# TODO: add recursion guard to prevent infinite loops
def serve(content='', end='\n', indent=0):
    """
    Prints content to stdout. Wrapper of print that provides special formatting
    for complex types.
    """
    if type(content) in [str, int, float]:
        print(content)
    elif type(content) in [list, set, frozenset, tuple]:
        indent += 4
        print('[')
        for i, item in enumerate(content):
            print(' '*indent, end='')
            print("[{}] ".format(i), end='')
            serve(item, indent=indent)
        indent -= 4
        print(' '*indent, end='')
        print(']')
    elif type(content) is dict:
        print('{')
        indent += 4
        for (key, value) in content.items():
            print(' '*indent, end='')
            print("{}: ".format(key), end='')
            serve(value, indent=indent)
        indent -= 4
        print(' '*indent, end='')
        print('}')
    # Helps with OrderedDict.
    elif hasattr(content, 'items'):
        serve(list(content.items()))
    # Stops objects like str from spewing everywhere.
    elif hasattr(content, '__dict__') and type(content.__dict__) is dict:
        serve(content.__dict__, end, indent=indent)
    elif hasattr(content, '_get_args()'):
        serve(list(content._get_args()), indent=indent)
    # When in doubt, use repr.
    else:
        print(repr(content), end=end)


def log(): pass 


class Response:
    """
    A `Response` object stores information about user input, taken as a response
    to a prompt. The object stores the input, after it has been verified and
    validated, as well as metadata about the input's context. The first word of
    the user's response, the command, or head, can be compared directly to the
    response object using '=='. A new response is generated for each input.
    """
    def __init__(self, head=None, body=None,
        raw_args=None, raw_kwargs=None, valid=False, empty=False, error=None):

        self.head = head if valid else None
        self.body = body
        if body is not None:
            for k, v in body.items():
                self.__dict__[k] = v

        # new params
        self.valid = valid
        self.empty = empty
        self.error = error
        self.raw_head = head
        self.raw_args = raw_args
        self.raw_kwargs = raw_kwargs

    def __eq__(self, x):
        """
        A `Response` will compare directly to a string, as in:
            response = malt.offer(options)
            if response == 'string':
                # do whatever
        If the response in invalid, either because of an unknown command or bad
        arguments, it will equate as `None`, not matching any strings. This way,
        if the user enters a known command, but mistyped arguments, the response
        will not match the command, and will not try to exec your code with
        incorrect arguments. Raw inputs can still be accessed manually, but do
        not affect equation operations.
        """
        return self.head == x

    def __str__(self):
        return self.raw_head
