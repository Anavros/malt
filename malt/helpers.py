
from os import system
from malt.malt import serve
from malt.exceptions import *

PREFIX = '[malt] '

# TODO: function to specify extra global helpers
def try_extra_functions(response, options, err=True):
    if response.raw_head == 'help':
        serve(options)
    elif response.raw_head == 'clear':
        system('clear')
    elif response.raw_head == 'quit':
        raise SystemExit
    elif response.error and err:
        print_error(response.error)


def print_error(error):
    t = type(error)
    if t is TooManyArgs:
        serve(PREFIX+"too many arguments")
    elif t is NotEnoughArgs:
        serve(PREFIX+"not enough arguments")
    elif t is UnknownCommand:
        serve(PREFIX+"unknown command (try 'help' for a list of commands)")
    elif t is EmptyCommand:
        serve("(empty)")
    elif t is InputForbiddenCharacters:
        serve(PREFIX+"input contains forbidden characters")
    elif t is WrongType:
        serve(PREFIX+"argument does not match expected type")
    elif t is NotAnOption:
        serve(PREFIX+"argument is not an option")
    else:
        serve(PREFIX+"unexpected error ({}: {})".format(str(t), str(error)))
