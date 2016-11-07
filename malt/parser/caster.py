
import re
from malt.exceptions import WrongType, BadTypePrefix, UnexpectedProgrammingError


# Typestring Regex
LIST_TYPE = r"^\[[sifb]\]$"
DICT_TYPE = r"\{[sifb]-[sifb]\}"


# TODO: Internal logging?
# TODO: Malt exceptions.
# TODO: Limited value types?
# TODO: Range types?
def autocast(value, typestring):
    """
    Cast a value to the type specified by a typestring.

    Typestrings can be 's': str, 'i': int, 'f': float, or 'b': bool.
    Lists of one type can be specified as '[i]'. Dicts contain a type for both
    key and value as '{s-i}'.

    Raises ValueError on impossible casts and BadTypePrefix when the given
    typestring doesn't match anything.
    """
    if typestring == 's':
        return value

    elif typestring == 'i':
        try:
            return int(value)
        except ValueError:
            raise WrongType(cast='i', value=value)

    elif typestring == 'f':
        try:
            return float(value)
        except ValueError:
            raise WrongType(cast='f', value=value)

    elif typestring == 'b':
        return (value != '0' and value.lower() != 'false')  # no errors

    elif re.fullmatch(LIST_TYPE, typestring):
        internal_cast = typestring.strip('[]')
        return [autocast(item, internal_cast) for item in value]

    elif re.fullmatch(DICT_TYPE, typestring):
        kc, vc = typestring.strip('{}').split('-', 1)
        return {autocast(k, kc):autocast(v, vc) for k, v in value.items()}

    else: raise BadTypePrefix(typestring)
