
import re
import shlex
import malt

def load(filepath, options):
    lines = []
    with open(filepath, 'r') as f:
        for raw_line in f:
            # clear out any comments or empty lines
            line = raw_line.split('#')[0].strip()
            if not line:
                continue
            pass

            # start doing things?
            (cmd, args) = parse(line, options)
            lines.append((cmd, args))
    return lines


def fill(options):
    arg_line = input()
    (cmd, args) = parse(arg_line)
    return Response(cmd, args)


def parse(arg_line, options):
    opt_line = match_option(arg_line, options)
    (cmd, values) = arg_parse(arg_line)
    (keys, casts) = opt_parse(opt_line)

    args = {}
    for key, value, cast in zip(keys, values, casts):
        if '(' in cast: # used for limited options: "arg:str(one|two|three)"
            halves = cast.split('(')
            cast = halves[0]
            allowed_values = halves[1].strip(')').split('|')
            args[key] = typecast(value, cast, allowed_values)
        else:
            args[key] = typecast(value, cast)

    #print(cmd)
    #malt.serve(args)
    return (cmd, args)
    #return Response(cmd, args)


def typecast(value, cast, allowed_values=None):
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


def match_option(arg_line, options):
    for opt_line in options:
        if shlex.split(arg_line)[0] == shlex.split(opt_line)[0]:
            return opt_line
    raise ValueError("Unknown command: {}.".format(shlex.split(arg_line)[0]))


#inp = "div id anchor:str(top|bottom|left|right) file size:float",
#cmd = "div"
#names = [id anchor file size]
#casts = [str str str float]
def opt_parse(opt_line):
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


#inp = "div main bottom nine.png 0.1"
#cmd = "div"
#arg = [main bottom nine.png 0.1]
def arg_parse(arg_line):
    arg_words = shlex.split(arg_line)
    return (arg_words[0], arg_words[1:])


#options = [
#    "div id anchor:str(top|bottom|left|right) file size:float",
#    "but id file",
#]
#
#opt = div + "id anchor:str(top|bottom|left|right) file size:float"
#bet = div + "id anchor file size"
#ipt = div + "main bottom nine.png 0.1"
#zip = div + [("id", "main"), ("anchor", "bottom"), ("file", "nine.png"), ("size", 0.1)]
#
#prototype = {
#    "div": {
#        "id": str,
#        "anchor": str,
#        "file": str,
#        "size": float,
#    },
#    "but": {
#        "id": str,
#        "file": str,
#    },
#}
#
#input = "div main bottom nine.png 0.1"
#result == "div"
#result.id == "main"
#result.anchor == "bottom"
#result.file == "nine.png"
#result.size == 0.1

if __name__ == '__main__':
    options = [
        "div id anchor:str(top|bottom|left|right) texture size:float"
    ]
    arg = "div main bottom"
    filepath = 'example.lang'
    malt.serve(load(filepath, options))
