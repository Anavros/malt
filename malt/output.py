
"""
Public functions for printing data to the terminal.
"""

from sys import stdout
from contextlib import contextmanager

from . import state
from .internal import mprint
from .formatting import form

redirections = { }


def serve(*items, end='\n', compact=False):
    """
    Print a number of items, of any type, to STDOUT, well formatted.

    Args:
        items: any number of items, similar to print()
        end (str): char to print after all items
        compact (bool): removes unnecessary brackets from list formatting
    """
    if len(items) == 0:
        mprint('\n')
    else:
        for item in items:
            mprint(form(item, end=end, compact=compact))


# TODO: Allow specific levels to redirect to specific files.
def log(*items, end='\n', compact=False, level='LOG', show_level=True):
    """
    Print items with an associated log level.

    Args:
        items: any number of printable items
        end (str): a character to print afterwards
        compact (bool): removes unnecessary brackets from list formatting
        level (str): a tag to associate with this message
        show_level (bool): prefix the message with its level
    """
    if level not in state.hidden_levels:
        global redirections
        file = redirections.get(level, None)
        if show_level:
            mprint(form('['+level+'] ', end=''), file)
        for item in items:
            mprint(form(item, end=end, compact=compact), file)


def redirect(level, file):
    """
    Set one log level to redirect to a given file-like object.
    If the given file is falsy, remove the redirection and default back to
    using STDOUT. Does not interfere with the level blacklist.
    """
    global redirections
    if file:
        redirections[level] = file
    else:
        try: del redirections[level]
        except KeyError: pass


# TODO: Bypass file redirects as well as blacklists.
@contextmanager
def showing(*levels):
    """
    Show new levels in addition to ones already shown within a block.

    Note:
        This is a contextmanager, to be used as ``with showing(levels)``.

    Args:
        levels: a list of levels to show within the with block, in addition to
            the levels already shown normally
    """
    restore = state.hidden_levels
    state.hidden_levels = set(levels|state.hidden_levels)
    yield
    state.hidden_levels = restore


def show(*levels):
    """
    Remove a logging level from the blacklist, if present.

    Levels are shown by default. ``show`` will only have an effect if a level
    has already been hidden using ``hide``.
    """
    for level in levels:
        if level in state.hidden_levels:
            state.hidden_levels.remove(level)


def hide(*levels):
    """
    Add a logging level to the blacklist, preventing it from being shown.
    """
    for level in levels:
        state.hidden_levels.add(level)
