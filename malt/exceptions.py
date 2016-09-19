
"""
malt.exceptions

Contains custom exceptions for parsing errors to prevent getting mixed up with
normal errors.
"""

class WrongType(TypeError):
    def __init__(self, cast='str', value=''):
        self.cast = cast
        self.value = value


class NotAnOption(TypeError):
    def __init__(self, value='', cast='str', options=None, bot=None, top=None):
        self.value = value
        self.cast = cast
        self.options = options if options is not None else []
        self.bot = bot
        self.top = top


class TooManyArgs(ValueError):
    pass


class NotEnoughArgs(ValueError):
    pass


class UnknownCommand(ValueError):
    pass


class EmptyCommand(ValueError):
    pass


class InputForbiddenCharacters(ValueError):
    pass


class UnexpectedProgrammingError(ValueError):
    pass
