
"""
Definitions of malt.offer() and malt.load().
Effectively compositions of lower-level parsing modules.
"""

from malt import parser
from malt.objects import Response
from malt.exceptions import MaltException


def parse(text, options):
    """
    Parse a single line of input.
    """
    try:
        available = parser.parse_options(options)
        userinput = parser.parse_user_input(text)
        expecting = parser.match_command(userinput, available)
        matched = parser.match_arguments(userinput, expecting)
        head, body = parser.cast(matched)
    except MaltException as e:
        return parser.handle(e, text)
    else:
        return Response(head, body, text)


def read(lines, options):
    """
    Parse a list of lines all at once. Returns a list of Response objects.
    """
    return [parse(line, options) for line in lines]


def offer(options):
    try:
        text = input('> ')
    except (KeyboardInterrupt, EOFError):
        raise SystemExit # silent exit without stack trace
    else:
        return parse(text, options)


# What about preprocessor steps?
def load(filepath, options):
    """
    Load and read a text file. Wrapper around read() that takes filename.
    """
    with open(filepath, 'r') as f:
        lines = f.readlines()
    return read(lines, options)
