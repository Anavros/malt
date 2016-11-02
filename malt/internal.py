
"""
Malt Internal Functions
Private functions for terminal input and output.
"""

from sys import stdout
from contextlib import contextmanager
from . import state, config


def iprint(item, continued=False):
    if not state.continuation:
        item = dent() + item
    print(item, end=('' if continued else '\n'))
    state.continuation = continued


def mprint(item, file=None):
    """
    """
    if file:
        # All file printing uses basic method.
        print(item, end='', file=file, flush=True)
    elif config.AUTOCLEAR:
        # Clear the screen for redrawing.
        # Can't use clear() because it will wipe the backlog.
        flush()
        # Autoclear is for interactive sessions.
        # It's easier to read and interact with, but not good for logs, etc.
        state.backlog += item
        print(state.backlog)
    else:
        # By default, just print.
        print(item, end='\n')


def minput():
    """
    Receive input from STDIN. Blocks thread. Maintains indent.
    """
    if state.header: print(dent() + state.header)
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
