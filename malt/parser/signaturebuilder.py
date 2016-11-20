
from malt.objects import Signature, Argument
from malt.exceptions import EmptyOptionString

"""
Take list of plain strings as options and generate signature objects.
Signatures are easier to use when validating input.
"""


example = [
    'keyword',
    'keyword argument',
    'keyword argument=default',
    'keyword i:int f:float s:string b:bool',
    'keyword [s]:list_of_strings {s-i}:map_of_strings_to_ints',
]
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
    sig = Signature(string)
    words = string.split()

    # Throw an error on empty strings.
    # Errors in this stage propogate up to caller code.
    # This is the caller's chance to verify their options are bug free,
    # before their program is in use.
    if not words:
        raise EmptyOptionString()

    # The first word in the option string is the command.
    # These are functionally different from the rest of the args.
    sig.head = words.pop(0)
    for word in words:
        # Split kwargs into keys and default values.
        if '=' in word:
            word, default = word.split('=', 1)
        else:
            word, default = word, None

        # Split type specifiers too.
        if ':' in word:
            cast, key = word.split(':', 1)
        else:
            cast, key = 's', word

        # TODO: what about casts?
        sig.add(key, value=default)

        # REMOVE:
        if default:
            sig.kwargs[key] = Argument(word, key, cast, default)
        else:
            sig.args.append(Argument(word, key, cast, default))
    return sig
