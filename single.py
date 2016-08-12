
import re
import shlex
import malt


"""Malt
A tiny toolkit for structured input and content.

Public Functions:
    offer
    serve
    harvest
"""

PROMPT = '> '

### PUBLIC FUNCTIONS ###


def offer(options):
    """Offer the user a list of options. Input is verified as returned as a
    Response object."""

    if not options or type(options) is not list:
        raise ValueError("Must offer a list of options!")

    cmd, args = _parse(input(PROMPT))
    return Response(cmd, args)
    # TODO built-in options


def harvest(filepath, options):
    """Load a config file matching syntax against given options."""

    lines = []
    with open(filepath, 'r') as f:
        for raw_line in f:
            # clear out any comments or empty lines
            line = raw_line.split('#')[0].strip()
            if not line:
                continue
            pass

            # start doing things?
            (cmd, args) = _parse(line, options)
            lines.append((cmd, args))
    return lines


def serve(content='', end='\n', indent=0):

    def more():
        return min(indent+4, 40)

    def less():
        return max(indent-4, 0)

    if type(content) in [str, int, float]:
        print(content, end=end)

    elif type(content) in [list, set, frozenset, tuple]:
        print('{} ['.format(str(type(content))[8:-2]))
        indent = more()
        for i, item in enumerate(content):
            print(' '*indent, end='')
            print("[{}] ".format(i), end='')
            serve(item, indent=indent)
        indent = less()
        print(' '*indent, end='')
        print(']')

    elif type(content) is dict:
        print('dict {')
        indent = more()
        for (key, value) in content.items():
            print(' '*indent, end='')
            print("{}: ".format(key), end='')
            serve(value)
        indent = less()
        print(' '*indent, end='')
        print('}')

    # Helps with OrderedDict.
    elif hasattr(content, 'items'):
        serve(list(content.items()))

    # Stops objects like str from spewing everywhere.
    elif hasattr(content, '__dict__') and type(content.__dict__) is dict:
        serve(content.__dict__, end)

    elif hasattr(content, '_get_args()'):
        serve(list(content._get_args()))

    # When in doubt, use repr.
    else:
        print(repr(content), end=end)


### INTERNAL FUNCTIONS ###


class Response(object):
    pass


def _parse(arg_line, options):
    opt_line = _match_option(arg_line, options)
    (cmd, values) = _arg_parse(arg_line)
    (keys, casts) = _opt_parse(opt_line)

    args = {}
    for key, value, cast in zip(keys, values, casts):
        if '(' in cast: # used for limited options: "arg:str(one|two|three)"
            halves = cast.split('(')
            cast = halves[0]
            allowed_values = halves[1].strip(')').split('|')
            args[key] = _typecast(value, cast, allowed_values)
        else:
            args[key] = _typecast(value, cast)

    #print(cmd)
    #malt.serve(args)
    return (cmd, args)
    #return Response(cmd, args)


def _typecast(value, cast, allowed_values=None):
    if allowed_values and value not in allowed_values:
        raise ValueError("{} is not an allowed value.".format(value))
        if cast == "str":
            value = str(value)
        elif cast == "int":
            value = int(value)
        elif cast == "float":
            value = float(value)
        else:
            raise ValueError("Unknown cast: {}.".format(cast))
    return value


def _match_option(arg_line, options):
    for opt_line in options:
        if shlex.split(arg_line)[0] == shlex.split(opt_line)[0]:
            return opt_line
    raise ValueError("Unknown command: {}.".format(shlex.split(arg_line)[0]))


#inp = "div id anchor:str(top|bottom|left|right) file size:float",
#cmd = "div"
#names = [id anchor file size]
#casts = [str str str float]
def _opt_parse(opt_line):
    opt_words = shlex.split(opt_line)
    cmd = opt_words.pop(0) # removes command from front
    names = []
    casts = []
    for opt in opt_words:
        halves = opt.split(':')
        # arg:type becomes arg, type
        if len(halves) == 2:
            name = halves[0]
            cast = halves[1]
        # default to str if no type is given
        elif len(halves) == 1:
            name = halves[0]
            cast = 'str'
        else:
            raise ValueError
        names.append(name) #?
        casts.append(cast)
    return (names, casts)


def _arg_parse(arg_line):
    arg_words = shlex.split(arg_line)
    return (arg_words[0], arg_words[1:])


if __name__ == '__main__':
    options = [
        "div id anchor:str(top|bottom|left|right) texture size:float"
    ]
    arg = "div main bottom"
    filepath = 'example.lang'
    serve(harvest(filepath, options))
