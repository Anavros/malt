
"""
Selects the matching signature for a given userinput.
"""

from malt.exceptions import UnknownCommand


def find(given, expected):
    """
    Given userinput and a dict of option signatures, select the signature that
    matches the userinput.
    """
    try:
        found = expected[given.head]
    except KeyError:
        raise UnknownCommand from None
    else:
        return found
