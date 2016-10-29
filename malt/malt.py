
from . import parse, state
from .internal import minput
from .exceptions import *

"""Malt
A tiny toolkit for structured input and output.
"""

def offer(options, leader=''):
    """Offer the user a list of options. Input is verified as returned as a
    Response object."""
    # TODO: extra function just to validate syntax
    # TODO: finish proper parser
    syntax = parse.parse(options)

    try:
        raw_text = minput()
    except (KeyboardInterrupt, EOFError):
        # Design point: Allow option to not exit immediately?
        # Put special variable in response and allow user?
        # Possibly extensible options where user can define built-in funcs?
        raise SystemExit  # silent

    # Hacky rough draft of command leader feature.
    if leader:
        if raw_text and raw_text[0] != leader:
            return Response(raw_text, noncommand=True)
        elif raw_text and raw_text[0] == leader:
            raw_text = raw_text[1:]

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
    except (WrongType, NotAnOption, TooManyArgs, NotEnoughArgs, UnknownKeyword) as e:
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


class Response:
    """
    A `Response` object stores information about user input, taken as a response
    to a prompt. The object stores the input, after it has been verified and
    validated, as well as metadata about the input's context. The first word of
    the user's response, the command, or head, can be compared directly to the
    response object using '=='. A new response is generated for each input.
    """
    def __init__(self, head=None, body=None,
        raw_args=None, raw_kwargs=None,
        valid=False, empty=False, error=None, noncommand=False):

        self.head = head if valid else None
        self.body = body
        if body is not None:
            for k, v in body.items():
                self.__dict__[k] = v

        # new params
        self.valid = valid
        self.noncommand = noncommand
        self.empty = empty
        self.error = error

        self.raw_head = head
        self.raw_args = raw_args if raw_args else []
        self.raw_kwargs = raw_kwargs if raw_kwargs else {}

    def __eq__(self, x):
        """
        Directly comparing a response to a string is being deprecated.
        Compare response.head instead.
        """
        return self.head == x

    def __str__(self):
        return self.raw_head
