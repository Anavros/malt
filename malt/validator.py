
from malt.caster import autocast

"""
Validation

Take each response, filled out with raw arguments, and verify that each
argument is in the right place.
"""


def validate(response, options):
    signatures = generate_signatures(options)
    try:
        sig = signatures[response.raw_head]
    except KeyError:
        response.valid = False
        print("KeyError: Unknown Command")
        return response
    try:
        response.finalize_args(compare_args(response, sig))
    except ValueError:
        print("ValueError: Arg Compairison")
    else:
        response.valid = True
        response.head = response.raw_head
    return response


#? keyword i:int
# keyword string
def compare_args(response, signature):
    validated = {}
    if len(response.raw_args) != len(signature.args):
        print("ValueError: Mismatched arg lengths!")
        raise ValueError()
    for r, s in zip(response.raw_args, signature.args):
        try:
            valid = autocast(r, s.cast)
        except ValueError as e:
            print("ValueError: Bad Cast ({})".format(e))
            raise
        else:
            print("Good Cast: "+str(valid))
            validated[s.key] = valid
    for key in signature.kwargs.keys():
        default = signature.kwargs[key]
        try:
            value = response.raw_kwargs[key]  # going to throw KeyError
        except KeyError:
            print("KeyError: Using Default Argument")
            value = default.default
            raise
        try:
            value = autocast(value, signature.kwargs[key].cast)
        except ValueError:
            print("ValueError: Bad Cast on Keyword Arg")
            raise
        validated[key] = value
    return validated


example = [
    'keyword',
    'keyword argument',
    'keyword argument=default',
    'keyword i:int f:float s:string b:bool',
    'keyword [s]:list_of_strings {s-i}:map_of_strings_to_ints',
]
def generate_signatures(options):
    signatures = {}
    for opt in options:
        sig = Signature(opt)
        words = opt.split()
        if len(words) < 1: raise ValueError()
        sig.head = words.pop(0)
        for word in words:
            if '=' in word:
                word, default = word.split('=', 1)
            else:
                word, default = word, None

            if ':' in word:
                cast, key = word.split(':', 1)
            else:
                cast, key = 's', word

            if default:
                sig.kwargs[key] = Argument(word, key, cast, default)
            else:
                sig.args.append(Argument(word, key, cast, default))
        signatures[sig.head] = sig
    return signatures


class Signature:
    def __init__(self, raw):
        self.raw = raw
        self.head = ""
        self.args = []
        self.kwargs = {}

    def __repr__(self):
        return "HEAD: {}, ARGS: {}, KWARGS: {}".format(
            self.head, self.args, self.kwargs)


class Argument:
    def __init__(self, raw, key, cast, default):
        self.raw = raw
        self.key = key
        self.cast = cast
        self.default = default

    def __repr__(self):
        if self.default:
            return "def={} ({})".format(self.default, self.cast)
        else:
            return "{} ({})".format(self.key, self.cast)
