
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
from . import state, config


# TODO: redirect to files, for logging.
def mprint(content, end=True):
    """
    Print to STDOUT. Maintains indentation level.
    """
    content = str(content)
    endchar = '\n' if end else ''
    if state.new_line:
        content = (' ' * state.tabs * config.tab_width) + content
    state.backlog += (content + endchar)
    if config.LEGACY_MODE:
        print(content, end=endchar)
    else:
        print('\n'*config.N_LINES)
        print(state.backlog)
    state.new_line = end


def minput():
    """
    Receive input from STDIN. Blocks thread.
    """
    if state.header: print(state.header)
    return input(config.PROMPT)


def clear():
    """
    OS-aware screen clearing.

    If config.ALIGN_TO_BOTTOM is set, clear() uses newlines instead of calling
    system clear, placing the user's cursor at the bottom of the term rather
    than the top.
    """
    state.backlog = ""
    if config.LEGACY_MODE:
        # TODO: windows
        os.system('clear')
    else:
        print('\n'*config.N_LINES)
