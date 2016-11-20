
from malt.objects import Signature, Argument
from malt.exceptions import EmptyOptionString

"""
Take list of plain strings as options and generate signature objects.
Signatures are easier to use when validating input.
"""


#example = [
#    'keyword',
#    'keyword argument',
#    'keyword argument=default',
#    'keyword i:int f:float s:string b:bool',
#    'keyword [s]:list_of_strings {s-i}:map_of_strings_to_ints',
#]

def generate_signatures(option_strings):
    """
    Convert a list of option strings to signatures. Returns a dictionary where
    keys are commands and values are signature objects.
    """
    signatures = [parse(string) for string in option_strings]
    return {s.head:s for s in signatures}
    # legibility hardmode:
    #{s.head:s for s in [parse(string) for string in option_strings]}


def parse(string):
    """
    Parse a single option string into a Signature object.
    """
    words = string.split()
    count = len(words)
    if count == 0:
        raise EmptyOptionString()
    elif count == 1:
        return Signature(words[0], [])
    else:
        head = words[0]
        tail = words[1:]
        body = []
        for index, castkeydefault in enumerate(tail):
            cast, key, default = separate(castkeydefault)
            body.append(Argument(index, key, default, cast))
        return Signature(head, body)


def separate(castkeydefault):
    # 'i:power=3' == cast:key=default == castkeydefault
    castkey, default = split_key_value(castkeydefault)
    cast, key = split_cast_key(castkey)
    return cast, key, default


def split_key_value(word):
    if '=' in word:
        return word.split('=', 1)
    else:
        return word, None


def split_cast_key(word):
    if ':' in word:
        return word.split(':', 1)
    else:
        # default to string cast, i.e. no cast
        return 's', word
