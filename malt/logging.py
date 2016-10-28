
from . import state
from .malt import serve

#levels = {
#    'LOG': sys.stdout
#}

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
