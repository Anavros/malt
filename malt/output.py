
from . import state
from .internal import mprint, indent
from .formatting import form

#levels = {
#    'LOG': sys.stdout
#}


def serve(x='', end=True, compact=True):
    print(form(x, compact=compact), end='')

# TODO: Add recursion guard to prevent infinite loops.
# TODO: Allow printing to file.
# TODO: Allow arbitrary numbers of args like print().
# TODO: Split into smaller, testable functions.
def oldserve(content='', end=True, compact=False):
    """
    Prints content to stdout. Wrapper of print that provides special formatting
    for complex types.
    """
    if type(content) in [str, int, float]:
        mprint(content, end=end)
    elif type(content) in [list, set, frozenset, tuple]:
        if not compact: mprint('[')
        with indent():
            for i, item in enumerate(content):
                mprint("[{}] ".format(i), end=False)
                serve(item, compact=compact)
        if not compact: mprint(']')
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


# TODO: Specify log levels to go to files instead of STDOUT.
# TODO: Show new levels by default, require blacklisting.
# IDEA: Context manager to show extra log level in `with` block.
# IDEA: Case insensitive levels?
def log(content, level='LOG', show_level=True):
    """
    Print content differently according to its level.
    If a level is blacklisted, using malt.silence('level'), it will not be
    printed. If show_level=True, each line will be prefixed by its level.
    """
    if level not in state.log_level_blacklist:
        if show_level:
            serve("[{}] ".format(level), end=False)
        serve(content)


def show(level):
    """
    Remove a logging level from the blacklist, if present.
    """
    if level in state.log_level_blacklist:
        state.log_level_blacklist.remove(level)


def silence(level):
    """
    Add a logging level to the blacklist, preventing it from being shown.
    """
    state.log_level_blacklist.add(level)
