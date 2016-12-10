
import re
from malt.constants import BRACES, JOIN
from malt.exceptions import WrongType, BadTypePrefix


# Typestring Regex
LIST_TYPE = r"^\[[sifb]\]$"
DICT_TYPE = r"\{[sifb]-[sifb]\}"


def cast(value, typestring):
    """
    Cast a value to the type specified by a typestring.

    Typestrings can be:
        's': str,
        'i': int,
        'f': float, or
        'b': bool.
    Lists of one type can be specified as '[i]'. Dicts contain a type for both
    key and value as '{s-i}'.

    Raises WrongType on impossible casts and BadTypePrefix when the given
    typestring doesn't match anything.
    """
    if typestring == 's':
        return value

    elif typestring == 'i':
        return _int(value)

    elif typestring == 'f':
        return _float(value)

    elif typestring == 'b':
        return _bool(value)

    elif re.fullmatch(LIST_TYPE, typestring):
        internal = typestring.strip('[]')
        return _list(value, internal)

    elif re.fullmatch(DICT_TYPE, typestring):
        keytype, valtype = typestring.strip('{}').split('-', 1)
        return _dict(value, keytype, valtype)

    else: raise BadTypePrefix(typestring)


def _int(string):
    try:
        # Cast to float first so strings like '1.0' don't throw errors.
        return int(float(string))
    except ValueError:
        raise WrongType(cast='i', value=string) from None


def _float(string):
    try:
        return float(string)
    except ValueError:
        raise WrongType(cast='f', value=string) from None


def _bool(string):
    return (string != '0' and string.lower() != 'false')  # no errors


def _list(string, internal):
    """
    Cast a string shaped like a list into an actual list. Recursively calls
    back to autocast to cast internal objects. Prevents nested lists.
    """
    result = []
    for value in string.strip(BRACES).split():
        result.append(cast(value, internal))
    return result


def _dict(string, keytype, valtype):
    """
    Cast a dict-shaped string into a dict. There can not be any spaces in the
    key:value pairs! This might be fixed in the future.
    """
    result = {}
    for item in string.strip(BRACES).split():
        key, val = item.split(JOIN)
        result[cast(key, keytype)] = cast(val, valtype)
    return result
