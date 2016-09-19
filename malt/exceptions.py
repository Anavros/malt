
"""
malt.exceptions

Contains custom exceptions for parsing errors to prevent getting mixed up with
normal errors.
"""

class WrongType(TypeError):
    pass


class NotAnOption(TypeError):
    pass


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
