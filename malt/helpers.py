
from malt.exceptions import *
from .output import serve
from .config import PREFIX


def print_error(error):
    t = type(error)
    if t is TooManyArgs:
        serve(PREFIX+"too many arguments")
    elif t is NotEnoughArgs:
        serve(PREFIX+"not enough arguments")
    elif t is UnknownKeyword:
        serve(PREFIX+"unknown keyword")
    elif t is UnknownCommand:
        serve(PREFIX+"unknown command (try 'help' for a list of commands)")
    elif t is EmptyCommand:
        serve("(empty)")
    elif t is InputForbiddenCharacters:
        serve(PREFIX+"input contains forbidden characters")
    elif t is WrongType:
        serve(PREFIX+"argument does not match expected type")
        serve(PREFIX+"failed to cast '{}' to type {}".format(error.value, error.cast))
    elif t is NotAnOption:
        serve(PREFIX+"argument is not an option")
        serve(PREFIX+"got '{}', expected {}:{} or ({}) (type {})".format(
            error.value, error.bot, error.top, '|'.join(error.options), error.cast))
    else:
        serve(PREFIX+"unexpected error ({}: {})".format(str(t), str(error)))
