
"""
Public functions for printing data to the terminal.
"""

from sys import stdout
from contextlib import contextmanager
from shutil import get_terminal_size

from . import state
from .internal import mprint, indent, iprint
from .formatting import form, choose_style

redirections = { }


def out(*items, continued=False, compact=True):
    for item in items:
        item, style = choose_style(item)
        if style == 'str':
            iprint(str(item), continued=continued)
        elif style == 'list':
            if len(item) < 1: iprint('[]')
            else: _print_list(item, compact)
        elif style == 'dict':
            if len(item) < 1: iprint('{}')
            else: _print_dict(item, compact)


def _print_list(item, compact):
    if not compact: iprint('[')
    with indent():
        for i, item in enumerate(item):
            iprint("[{}] ".format(i), continued=True)
            out(item, compact=compact)
    if not compact: iprint(']')


def _print_dict(item, compact):
    if not compact: iprint('{')
    with indent():
        for (key, value) in sorted(item.items()):
            iprint("{}: ".format(key), continued=True)
            out(value, compact=compact)
    if not compact: iprint('}')


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


def old_serve(content='', end=True):
    """
    Prints content to stdout. Wrapper of print that provides special formatting
    for complex types.
    """
    if type(content) in [str, int, float]:
        mprint(content, end=end)
    elif type(content) in [list, set, frozenset, tuple]:
        #indent += 4
        mprint('[')
        with indent():
            for i, item in enumerate(content):
                mprint("[{}] ".format(i), end=False)
                serve(item)
        mprint(']')
    elif type(content) is dict:
        mprint('{')
        with indent():
            for (key, value) in content.items():
                mprint("{}: ".format(key), end=False)
                serve(value)
        mprint('}')
    # Helps with OrderedDict.
    elif hasattr(content, 'items'):
        serve(list(content.items()))
    # Stops objects like str from spewing everywhere.
    elif hasattr(content, '__dict__') and type(content.__dict__) is dict:
        serve(content.__dict__, end)
    elif hasattr(content, '_get_args()'):
        serve(list(content._get_args()))
    # When in doubt, use repr.
    else:
        mprint(repr(content), end)
