
"""
malt.exceptions

Contains custom exceptions for parsing errors to prevent getting mixed up with
normal errors.
"""

# Errors raised on user input.
class WrongType(TypeError):
    """ A given value can not be casted to the expected type. """
    def __init__(self, cast='str', value=''):
        self.cast = cast
        self.value = value
        self.message = '[malt] argument does not match expected type'


class NotAnOption(TypeError):
    """
    Deprecated for now: User input is not in the explicitly allowed options.
    """
    def __init__(self, value='', cast='str', options=None, bot=None, top=None):
        self.value = value
        self.cast = cast
        self.options = options if options is not None else []
        self.bot = bot
        self.top = top


class TooManyArgs(ValueError):
    """ The user's input has too many arguments. """


class NotEnoughArgs(ValueError):
    """ The user's input is missing arguments. """


class UnknownKeyword(ValueError):
    pass


class UnknownCommand(ValueError):
    """
    Ther user has given a command that is not included in the supplied options.
    """


class EmptyCommand(ValueError):
    """ The user has entered an empty line. """


class InputForbiddenCharacters(ValueError):
    pass


# Errors raised when parsing option arrays.
class BadTypePrefix(ValueError):
    """ Unknown or misformatted type prefix in supplied options. """
    def __init__(self, typestring):
        self.typestring = typestring


# General mishaps.
class UnexpectedProgrammingError(ValueError):
    """
    Something unexpected happened due to programming error and not user input.
    """
