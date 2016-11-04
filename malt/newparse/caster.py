

import re
#from .exceptions import WrongType, NotAnOption, UnexpectedProgrammingError


# Typestring Regex
LIST_TYPE = r"^\[[sifb]\]$"
DICT_TYPE = r"\{[sifb]-[sifb]\}"


def autocast(value, typestring):
    print(typestring)
    if typestring == 's':
        return value
    elif typestring == 'i':
        return int(value)
    elif typestring == 'f':
        return float(value)
    elif typestring == 'b':
        return bool(value)
    elif re.fullmatch(LIST_TYPE, typestring):
        internal_cast = typestring.strip('[]')
        return [autocast(item, internal_cast) for item in value]
    elif re.fullmatch(DICT_TYPE, typestring):
        print(typestring)
        key_cast, value_cast = typestring.strip('{}').split('-', 1)
        print(key_cast, value_cast)
        return {autocast(k, key_cast):autocast(v, value_cast) for k, v in value.items()}
    else:
        print("ValueError: Bad Typestring")
