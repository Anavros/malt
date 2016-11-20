
from malt.objects import Argument, Signature
from malt.exceptions import TooManyArgs, NotEnoughArgs
from malt.parser.specifier import generate_signatures
from malt.parser.caster import autocast  # TODO: Remove

"""
Take each response, filled out with raw arguments, and verify that each
argument is in the right place, and typecast too.
"""


# TODO: separate typecasting
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
        print("ValueError: Arg Comparison")
    else:
        response.valid = True
        response.head = response.raw_head
    return response

# res = [arg1 arg2 arg3] {key4:nondefault}  # key5 is missing
# sig = [key1 key2] {key3:arg3 key4:arg4 key5:arg5}
def tally(args, kwargs, need, kwneed):
    pass


#response = [
#    (None, 'val1'),
#    (None, 'val2'),
#    (key3, 'otherval3'),
#]
#signature = [
#    (key1, None),
#    (key2, None),
#    (key3, 'val3'),
#    (key4, 'val4'),
#]
def map_arguments(response, signature):
    mappings = {}
    if len(response) != len(signature):
        raise ValueError()
    for i, (key, value) in enumerate(response):
        if key is None:
            key = signature[i][0]
        # Losing positional information when putting into normal dictionary.
        mappings[key] = value


#? keyword i:int
# keyword string
def compare_args(response, signature):
    validated = {}
    # BUG: Kwargs without keys will show up in response.raw_args!
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
            #raise
        try:
            value = autocast(value, signature.kwargs[key].cast)
        except ValueError:
            print("ValueError: Bad Cast on Keyword Arg")
            raise
        validated[key] = value
    return validated
