
from .malt import offer, load, serve
from .logging import log, show, silence
from .internal import clear, indent

try:
    import readline
except ImportError:
    pass

def set_header(text):
    state.header = text
