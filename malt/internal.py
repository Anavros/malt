
"""
Malt Internal Functions
Private functions for terminal input and output.

Details:
-> mprint()
Wrapper around print() that maintains indentation level.
-> minput()
Same for input() that enables indent, headers, and spacing.
-> clear()
OS-aware screen clearing. If config.ALIGN_TO_BOTTOM is set, clear() uses
newlines instead of calling system clear, placing the user's cursor at the
bottom of the term rather than the top.
"""

import os
from contextlib import contextmanager
from . import state, config


# TODO: redirect to files, for logging.
def mprint(something, end=True):
    """
    Print to STDOUT. Maintains indentation level.
    """
    # Clear the screen for redrawing.
    # Can't use clear() because it will wipe the backlog.
    flush()
    something = str(something) + ('\n' if end else '')
    if state.new_line:
        something = dent() + something
    state.backlog += (something)
    state.new_line = end
    print(state.backlog)


def minput():
    """
    Receive input from STDIN. Blocks thread. Maintains indent.
    """
    if state.header:
        print(dent() + state.header)
    return input(dent() + config.PROMPT)


def dent():
    return ' ' * state.tabs * config.tab_width


@contextmanager
def indent():
    state.tabs += 1
    yield
    state.tabs -= 1


def flush():
    """
    Print a large number of newlines to force the cursor to the bottom.
    """
    print('\n'*config.N_LINES)


def clear():
    """
    Flush the screen as well as remove the backlog. Callable by the user.
    """
    state.backlog = ""
    flush()
