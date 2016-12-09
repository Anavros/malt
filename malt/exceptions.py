
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
        self.message = "unable to cast '{}' to type({})".format(
            value, cast)


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


class MismatchedArgs(ValueError):
    """ User input has either too many or too few arguments. """
    def __init__(self):
        self.message = "wrong number of arguments"


class MissingValue(ValueError):
    """ User input is missing a required argument. """
    def __init__(self):
        self.message = "missing positional values"


class AmbiguousArgs(ValueError):
    """ User arguments can not be ordered, likely due to kwargs out of place. """
    def __init__(self):
        self.message = "positional arg found after kwarg"


class UnknownKeyword(ValueError):
    """ User input contains a known command, but unknown argument keys. """
    def __init__(self, keyword=''):
        self.message = "unknown keyword argument"


class UnknownCommand(ValueError):
    """
    Ther user has given a command that is not included in the supplied options.
    """
    def __init__(self, command=''):
        self.message = "unknown command"


class EmptyCommand(ValueError):
    """ The user has entered an empty line. """
    def __init__(self):
        self.message = "empty line"


class MaltSyntaxError(ValueError):
    """ The parser has encountered incorrect syntax and can not continue. """
    def __init__(self, details=''):
        self.details = details
        # TODO: line numbers for easier debugging
        self.message = "syntax error on input: " + details


# Errors raised when parsing option arrays.
class BadTypePrefix(ValueError):
    """ Unknown or misformatted type prefix in supplied options. """
    def __init__(self, typestring):
        self.typestring = typestring


class EmptyOptionString(ValueError):
    """ An option string was completely empty. """
    def __init__(self):
        self.message = "unknown command"


# General mishaps.
class UnexpectedProgrammingError(ValueError):
    """
    Something unexpected happened due to programming error and not user input.
    """
