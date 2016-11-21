
"""
Definitions of malt.offer() and malt.load().
Effectively compositions of lower-level parsing modules.
"""

from malt import parser
from malt.exceptions import *


def offer(options):
    try:
        text = input('> ')
    except (KeyboardInterrupt, EOFError):
        raise SystemExit # silent exit without stack trace
    else:
        return parse(text, options)


def parse(text, options):
    """
    Parse a single line of input.
    """
    try:
        available = parser.parse_options(options)
        userinput = parser.parse_user_input(text)
        expecting = parser.match_command(userinput, available)
        matched = parser.match_arguments(userinput, expecting)
        response = parser.cast(matched)
    except (EmptyOptionString, MaltSyntaxError, UnknownCommand, UnknownKeyword,
        MissingValue, WrongType) as e:
        return parser.handle(e)
    else:
        return response


def read(lines, options):
    return [parse(line, options) for line in lines]


def load(filepath, options):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    return read(lines, options)


def check_syntax(options):
    """
    Optional function to verify a given option list is usable.
    """
    # Raises errors if any problems are found.
    signaturebuilder.generate_signatures(options)
