
import re
import shlex
import malt


"""Malt
A tiny toolkit for structured input and output.

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


def serve(output='', nl=True):
    """Print something to the console with smart formatting.

    Accepts one item at a time to print to the console. Items are checked by
    type and available attributes to determine the best way to format them.
    Generally speaking, output should be much more readable that the basic
    print function. Supports indentation.
    """
    if type(output) in [str, int, float]:
        _mprint(output, nl)

    # NOTE: nested tuples render as str(tuple)
    elif type(output) is tuple:
        if not output:
            _mprint('()')
        else:
            _mprint('(', nl=False)
            for item in output[:-1]:
                _mprint(str(item)+', ', nl=False)
            _mprint(str(output[-1]), nl=False)
            _mprint(')', nl)

    elif type(output) in [list, set, frozenset]:
        _mprint('[', nl=output)
        with indent():
            for i, item in enumerate(output):
                if not _fresh_line:
                    _mprint()
                #_mprint(LIST_TICK, nl=False)
                _mprint("[{}] ".format(i), nl=False)
                serve(item)
        _mprint(']', nl)

    elif type(output) is dict:
        _mprint("{", nl=output)
        with indent():
            for (key, value) in output.items():
                _mprint("{}: ".format(key), nl=False)
                serve(value)
        _mprint("}")

    # Helps with OrderedDict.
    elif hasattr(output, 'items'):
        serve(list(output.items()))

    # Stops objects like str from spewing everywhere.
    elif hasattr(output, '__dict__') and type(output.__dict__) is dict:
    #elif hasattr(output, '__dict__'):
        serve(output.__dict__, nl)

    elif hasattr(output, '_get_args()'):
        serve(list(output._get_args()))

    # When in doubt, use repr.
    else:
        _mprint(repr(output), nl)


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
