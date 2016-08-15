
import re
import os
import shlex


"""Malt
A tiny toolkit for structured input and output.
"""

PREFIX = '[malt] '
PROMPT = '> '

# Hardcoded Character Markers
c_COMMENT = '#'
c_SYNTAX = '?'
c_TYPE_SPLIT = ':'
c_KEYWORD_SPLIT = '|'
c_LEFT_BRACKET = '('
c_RIGHT_BRACKET = ')'

class ParseError(ValueError):
    def __init__(self, code):
        self.code = code
    EMPTY, ARG_COUNT, ARG_TYPE, COMMAND, HELP, CLEAR, QUIT = range(7)

### PUBLIC FUNCTIONS ###


def offer(options):
    """Offer the user a list of options. Input is verified as returned as a
    Response object."""
    if not options or type(options) is not list:
        raise ValueError("Must offer a list of options!")

#    if _valid_syntax(options):
#        word = _valid_syntax(options) #TODO
#        raise ValueError("Malformed option syntax!", word)

    try:
        cmd, args = _parse(input(), options)
    except ParseError as e:
        _handle(e.code)
        return Response(None)
    except (KeyboardInterrupt, EOFError):
        _quit()
    else:
        return Response(cmd, args)


def _handle(code):
    if code == ParseError.HELP:
        _help()
    elif code == ParseError.CLEAR:
        _clear()
    elif code == ParseError.QUIT:
        _quit()
    elif code == ParseError.EMPTY:
        print("Error.")
    elif code == ParseError.ARG_COUNT:
        print("Error.")
    elif code == ParseError.ARG_TYPE:
        print("Error.")
    elif code == ParseError.COMMAND:
        print("Error.")
    else:
        raise ValueError("Unknown error code.")


def _valid_syntax(syntax):
    word_form = r"^([a-z_0-9]+)(:(str|int|float)(\([a-z_|0-9]*\))?)?$"
    for line in syntax:
        for word in line.split():
            if not re.match(word_form, word):
                return word
    return None


class Syntax(object):
    def __init__(self, cmd, arg_count, keys, casts):
        pass

    def match(response):
        pass


def _re_do(options):
    if not options or type(options) is not list:
        raise ValueError("Must provide a valid list of options!")

    form = r"""
    ^
    ([a-z_0-9]+)        # \1 Required command name.
    (:(str|int|float)   # \2 Optional type specifier separated by a colon.
    (\([a-z_|0-9]*\)    # \3 Optional pipe-separated list of allowed values.
    )?
    )?
    $
    """
    for line in options:
        match = re.match(form, line, re.VERBOSE)
        if not match:
            raise ValueError("Must provide a valid list of options!")


def harvest(filepath, options=None):
    """Load a config file matching syntax against given options."""
    lines = []
    if not options: # must be in lang file
        options = _harvest_syntax(filepath)
        if not options: # still
            raise Exception("Language syntax not provided or found in file.")
    with open(filepath, 'r') as f:
        for raw_line in f:
            # clear out any comments or empty lines
            line = raw_line.split(c_COMMENT)[0].strip()
            if not line:
                continue
            if line[0] == c_SYNTAX:
                continue
            # start doing things?
            (cmd, args) = _parse(line, options)
            lines.append((cmd, args))
    return lines


def _harvest_syntax(filepath):
    syntax = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            if line[0] == c_SYNTAX:
                line = line.strip(c_SYNTAX).strip()
                syntax.append(line)
    return syntax


def serve(content='', end='\n', indent=0):
    def more():
        return min(indent+4, 40)
    def less():
        return max(indent-4, 0)
    if type(content) in [str, int, float]:
        print(content)
    elif type(content) in [list, set, frozenset, tuple]:
        indent = more()
        print('[')
        for i, item in enumerate(content):
            print(' '*indent, end='')
            print("[{}] ".format(i), end='')
            serve(item, indent=indent)
        indent = less()
        print(' '*indent, end='')
        print(']')
    elif type(content) is dict:
        print('{')
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


def _help(options):
    indent = 0
    def more():
        return min(indent+4, 40)
    def less():
        return max(indent-4, 0)
    print(PREFIX + "Available Options:")
    indent = more()
    for i, opt_line in enumerate(options):
        (cmd, keys, casts) = _opt_parse(opt_line)
        print(' '*indent, end='')
        print('[{}] {}'.format(i, cmd))
        indent = more()
        for key, cast in zip(keys, casts):
            print(' '*indent, end='')
            print("- {}: {}".format(key, cast))
        indent = less()
    indent = less()


def _quit():
    raise SystemExit


def clear():
    os.system("cls" if os.name == "nt" else "clear")


class Response(object):
    def __init__(self, cmd=None, args=None):
        self.cmd = cmd
        if args is not None:
            for k, v in args.items():
                self.__dict__[k] = v
    def __eq__(self, string):
        return self.cmd == string


def _deconstruct_options(options):
    result = []
    for opt_line in options:
        opt_words = shlex.split(opt_line) # preserve quoted strings
        cmd = opt_words.pop(0)
        keys = []
        casts = []
        for opt in opt_words:
            # param:str(top|bottom|left|right)
            # param:int(a|b|c|d) XXX avoid? mismatched types
            # param:int:float XXX too many, throw error
            if c_TYPE_SPLIT in opt:
                # param:int
                halves = opt.split(c_TYPE_SPLIT)
                keys.append(halves[0])
                casts.append(halves[1])
            else:
                # param
                keys.append(opt)
                casts.append('str')
        result.append((cmd, keys, casts))
    return result


def _parse(arg_line, options):
    cmd, values = _arg_parse(arg_line)
    opt_line = _match_option(cmd, options)
    if not opt_line:
    _, keys, casts = _opt_parse(opt_line)



    if len(values) != len(keys):
        raise ParseError(ParseError.ARG_COUNT, given=len(values), expected=len(keys))

    args = {}
    for key, value, cast in zip(keys, values, casts):
        if c_LEFT_BRACKET in cast: # used for limited options: "arg:str(one|two|three)"
            halves = cast.split(c_LEFT_BRACKET)
            cast = halves[0]
            allowed_values = halves[1].strip(c_RIGHT_BRACKET).split(c_KEYWORD_SPLIT)
            args[key] = _typecast(value, cast, allowed_values) # may throw ParseError
        else:
            args[key] = _typecast(value, cast)
    return (cmd, args)


def _cut(line, char):
    return line.split(char)[0].strip()


def _match_option(arg, options):
    for line in options:
        if line.split()[0] == arg.split()[0]:
            return line
    # if not found
    raise ParseError(ParseError.COMMAND)


# TODO: parse options when given, not every time args need to be matched.
# This way we can raise errors for bad option args, which are programmer errors,
# when the program starts, and not when the user is using it.
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
            pass # TODO above note
        names.append(name)
        casts.append(cast)
    return (cmd, names, casts)


def _arg_parse(arg_line):
    arg_words = shlex.split(_cut(arg_line, c_COMMENT))
    # KeyError on len() == 1? XXX
    return (arg_words[0], arg_words[1:])


def _typecast(value, cast, allowed_values=None):
    if allowed_values and value not in allowed_values:
        raise ParseError(ParseError.TYPE)
    if cast == "str":
        value = str(value)
    elif cast == "int":
        value = int(value)
    elif cast == "float":
        value = float(value)
    else:
        raise ParseError(ParseError.TYPE)
    return value


def _firsts(list_of_strings):
    return [shlex.split(string)[0] for string in list_of_strings]
