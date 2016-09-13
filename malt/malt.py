
import re
import malt.parse as parse

try:
    import readline
except ImportError:
    pass

"""Malt
A tiny toolkit for structured input and output.
"""

PREFIX = '[malt] '
PROMPT = '> '

### PUBLIC FUNCTIONS ###

def offer(options):
    """Offer the user a list of options. Input is verified as returned as a
    Response object."""
    syntax = parse.parse(options)

    try:
        raw_text = input(PROMPT)
    except (KeyboardInterrupt, EOFError):
        quit()
    if not raw_text:
        return Response(None, None, raw_args=None, raw_kwargs=None, valid=False)

    try:
        head, args, kwargs = parse.parse_response(raw_text)
    except ValueError:
        return Response(head, None, raw_args=args, raw_kwargs=kwargs, valid=False)

    try:
        syn = syntax[head]
    except KeyError:
        return Response(head, None, raw_args=args, raw_kwargs=kwargs, valid=False)

    try:
        body = parse.validate((args, kwargs), syn)
    except ValueError as e:
        return Response(head, None, raw_args=args, raw_kwargs=kwargs, valid=False)
    return Response(head, body, raw_args=args, raw_kwargs=kwargs, valid=True)


def load(filepath, options=None):
    """Load a config file matching syntax against given options."""
    if options:
        syntax = parse.parse(options)
    else:
        syntax = parse.parse(_syntax_hints(filepath))
    responses = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.split('#')[0].strip()
            line = line.split('?')[0].strip()
            if not line: continue

            head, raw_args, raw_kwargs = parse.parse_response(line)
            body = parse.validate((raw_args, raw_kwargs), syntax[head])

            #print("SYNTAX")
            #serve(syntax)
            #print("HEAD")
            #serve(head)
            #print("BODY")
            #serve(body)
            responses.append(Response(head, body))
    return responses


def serve(content='', end='\n', indent=0):
    """Prints easy-to-read data structures according to type."""
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


class Response:
    """
    A `Response` object stores information about user input, taken as a response
    to a prompt. The object stores the input, after it has been verified and
    validated, as well as metadata about the input's context. The first word of
    the user's response, the command, or head, can be compared directly to the
    response object using '=='. A new response is generated for each input.
    """
    def __init__(self, head, body, raw_args=None, raw_kwargs=None, valid=False):
        self.head = head if valid else None
        self.valid = valid
        if body is not None:
            for k, v in body.items():
                self.__dict__[k] = v

        # new params
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
