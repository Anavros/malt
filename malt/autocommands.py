
from .internal import clear
from .output import serve
from .helpers import print_error  # temporary


def show_options(r):
    serve("Options:")
    serve(r.options, compact=True)
    serve()
    serve("Auto-Options (Available Everywhere):")
    serve(list(included.keys()), compact=True)
    if supplied:
        serve()
        serve(list(supplied.keys()), compact=True)

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
