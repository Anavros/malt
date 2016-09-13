
from os import system
from malt.malt import serve


# TODO: function to specify extra global helpers
def try_extra_functions(response, options):
    if response.raw_head == 'help':
        serve(options)
    elif response.raw_head == 'clear':
        system('clear')
    elif response.raw_head == 'quit':
        raise SystemExit
