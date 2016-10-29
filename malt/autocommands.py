
from .internal import clear
from .output import serve
from .helpers import print_error  # temporary


def show_options():
    serve("OPTIONS")


def quit():
    raise SystemExit


# Dicts must come after declarations because they are defined on import!
included = {
    'help': show_options,
    'clear': clear,
    'quit': quit,
}
supplied = {
}

def handle(response):
    if response.raw_head in supplied.keys():
        supplied[response.raw_head]()
    elif response.raw_head in included.keys():
        included[response.raw_head]()
    elif response.error:
        print_error(response.error)
