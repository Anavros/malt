
from .internal import clear, indent, iprint
from .helpers import print_error  # temporary


def show_options(r):
    iprint("Options:")
    with indent():
        for o in r.options:
            iprint(o)
    iprint('')
    iprint("Auto-Options (Available Everywhere):")
    with indent():
        for k in included.keys():
            iprint(k)
    if supplied:
        with indent():
            for k in supplied.keys():
                iprint(k)

def clear_screen(r): clear()
def quit(r): raise SystemExit


# Dicts must come after declarations because they are defined on import!
included = {
    'help': show_options,
    'clear': clear_screen,
    'quit': quit,
}
supplied = {
}

def handle(response):
    if response.raw_head in supplied.keys():
        supplied[response.raw_head](response)
    elif response.raw_head in included.keys():
        included[response.raw_head](response)
    elif response.error:
        print_error(response.error)
