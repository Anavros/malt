
#from .malt import offer, load
#from .output import serve, log, show, hide, redirect, showing, out
#from .internal import clear, indent
#from .autocommands import handle

try: import readline
except ImportError: pass
from .io import parse, offer

#def set_header(text):
    #state.header = '\n'.join([line.strip() for line in text.split('\n')])


#def autocommand(commands):
    #if type(commands) is not dict: raise ValueError()
    #autocommands.supplied = commands
