
"""
Validation

Take each response, filled out with raw arguments, and verify that each
argument is in the right place.
"""


def validate(responses, options):
    signatures = generate_signatures(options)
    for response in responses:
        try:
            sig = signatures[response.raw_head]
        except KeyError:
            response.valid = False
            raise
        try:
            compare_args(response.raw_args, sig.args)
        except ValueError:
            raise
    return responses


#? keyword i:int
# keyword string
def compare_args(response_args, signature_args):
    validated = {}
    for r, s in zip(response_args, signature_args):
        try:
            #valid = caster.cast(r, s.cast)
            valid = "STAND-IN"
        except ValueError:
            raise
        else:
            validated[s.key] = valid
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
