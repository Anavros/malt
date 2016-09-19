
from .malt import offer, load, serve
import malt.internal

try:
    import readline
except ImportError:
    pass

def bless():
    try:
        import blessings
    except ImportError:
        pass
    else:
        malt.internal.blessed = True
