
from .malt import offer, load
from .output import serve, log, show, silence
from .internal import clear, indent
from .autocommands import handle

try:
    import readline
except ImportError:
    pass

def set_header(text):
    state.header = text


def autocommand(commands):
    if type(commands) is not dict: raise ValueError()
    autocommands.supplied = commands
