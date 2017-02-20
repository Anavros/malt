
"""
Definitions of malt.offer() and malt.load().
Effectively compositions of lower-level parsing modules.
"""

from malt import parser
from malt.objects import Response
from malt.exceptions import MaltException

#import logging
#logging.basicConfig(filestring="parser.log", level=logging.DEBUG)
#logging.info("cmd.py loaded")


def _convert_to_signatures(options):
    """
    Convert a list of strings into signature objects.
    """
    if type(options) is not list:
        raise ValueError("Options must be a list of strings.")
    return parser.parse_options(options)


def parse(text, options, silent=False, convert=True):
    """
    Parse a single line of input.
    """
    # Temporary measure to avoid breaking interface.
    if convert:
        signatures = _convert_to_signatures(options)
    else:
        signatures = options
    try:
        # This takes a list of option strings and creates a list of signatures.
        # Add another function to accept option objects, not strings.
        available = parser.parse_options(options)
        userinput = parser.parse_user_input(text)
        expecting = parser.match_command(userinput, available)
        matched = parser.match_arguments(userinput, expecting)
        head, body = parser.cast(matched)
    except MaltException as e:
        if not silent:
            print("[malt]", str(e))
        return Response("", {}, text)
    else:
        return Response(head, body, text)


def read(lines, options, silent=False):
    """
    Parse a list of lines all at once. Returns a list of Response objects.
    """
    if type(lines) is str:
        raise ValueError("Read requires a list of strings, not a single string.")
    responses = []
    for line in lines:
        #logging.debug("Reading line: {}".format(line))
        # TODO: this should be a preprocessor step
        line = line.strip()
        if not line:
            continue

        #logging.debug("Parsing modified line: {}".format(line))
        responses.append(parse(line, options, silent))
    return responses


def offer(options, silent=False):
    try:
        text = input('> ')
    except (KeyboardInterrupt, EOFError):
        raise SystemExit # silent exit without stack trace
    else:
        return parse(text, options, silent)


# What about preprocessor steps?
# TODO: Raise error if file doesn't exist? or just propagate?
def load(filepath, options, silent=False):
    """
    Load and read a text file. Wrapper around read() that takes filename.
    """
    with open(filepath, 'r') as f:
        text = f.read()
    text = parser.preprocess(text)
    # should read take a list or a newline separated string?
    return read(text.split('\n'), options, silent)
