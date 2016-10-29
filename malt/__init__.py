
from .malt import offer, load, serve, indent
from .logging import log, show, silence
from .internal import clear

try:
    import readline
except ImportError:
    pass

def set_header(text):
    state.header = text
