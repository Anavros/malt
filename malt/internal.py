
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
    print(content, end=endchar)
    state.new_line = end


# IDEA: Autoclear after `n` commands.
# Store output in a list and when you autoclear, redraw that output.
def minput():
    """
    Receive input from STDIN. Blocks thread.
    """
    print('\n'*config.SPACING_LINES, end='')
    if state.show_new_header and state.new_header:
        print(state.new_header)
    return input(config.PROMPT)


def clear():
    """
    OS-aware screen clearing.

    If config.ALIGN_TO_BOTTOM is set, clear() uses newlines instead of calling
    system clear, placing the user's cursor at the bottom of the term rather
    than the top.
    """
    if config.ALIGN_TO_BOTTOM:
        print('\n'*config.CLEAR_NEWLINES)
    else:
        # TODO: windows
        os.system('clear')
