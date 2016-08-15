
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

r_SYNTAX_FORM_X = r"""
^
(?P<key> \w+)               # Required argument name.
(:                          # Don't match the colon.
(?P<cast> (str|int|float)   # Optional type specifier separated by a colon.
(?P<allow> \([a-z_|0-9]*\)  # Optional pipe-separated list of allowed values.
)?
)
)?
$
"""

r_SYNTAX_FORM = r"""
^
(?P<cast>(str|int|float))?
 (?(cast) \( )
(?P<key>[a-z]+)
 (?(cast) \) )
(?P<allow>\[[\w\d_|]+\])?
$
"""

### PUBLIC FUNCTIONS ###


def offer(options):
    """Offer the user a list of options. Input is verified as returned as a
    Response object."""

    # Throws ValueError on bad options before the user gives input.
    # Alerts the programmer without surprising the user.
    allowed_syntaxes = _compile(options)

    try:
        given_args = shlex.split(input(PROMPT))
    except (KeyboardInterrupt, EOFError):
        _quit()
    if not given_args:
        return Response(None)
    command = given_args.pop(0)

    try:
        expected_args = _get_args(command, allowed_syntaxes)
    except ValueError:
        if command == 'help':
            _help(allowed_syntaxes)
        elif command == 'clear':
            clear()
        elif command == 'quit':
            _quit()
        else:
            print("unknown command")
        return Response(None)

    try:
        final_args = _verify_arguments(given_args, expected_args)
    except ValueError:
        print("bad typing or something!")
        return Response(None)
    else:
        return Response(command, final_args)


class Argument(object):
    def __init__(self, key, cast='str', values=None, comment=None):
        self.key = key
        self.cast = cast
        self.values = values
        self.comment = comment


class Response(object):
    def __init__(self, cmd, args=None):
        self.cmd = cmd
        if args is not None:
            for k, v in args.items():
                self.__dict__[k] = v
    def __eq__(self, string):
        return self.cmd == string


def _compile(options):
    if not options or type(options) is not list:
        raise ValueError("Must provide a valid list of options!")
    allowed_syntaxes = []
    for line in options:
        words = line.split()
        # Command
        cmd = _match_cmd(words.pop(0))
        args = []
        for word in words:
            key, cast, allow = _match_arg(word)
            args.append(Argument(key, cast, allow))
        allowed_syntaxes.append((cmd, args))
    return allowed_syntaxes


def _match_cmd(word):
    match = re.fullmatch(r_SYNTAX_FORM, word, re.VERBOSE)
    if not match:
        raise ValueError("Malformed command: {}.".format(word))
    if match.group('cast') or match.group('allow'):
        raise ValueError("Can not cast commands, only args.")
    else:
        return match.group('key')


def _match_arg(word):
    match = re.fullmatch(r_SYNTAX_FORM, word, re.VERBOSE)
    if not match:
        raise ValueError("Malformed argument: {}.".format(word))
    key = match.group('key')
    cast = match.group('cast')
    if cast is None:
        cast = 'str'
    allow = match.group('allow')
    if allow:
        allow = allow.strip('[]').split('|')
    return key, cast, allow


def _get_args(user_cmd, allowed_syntaxes):
    for (cmd, args) in allowed_syntaxes:
        if user_cmd == cmd:
            return args
    # if not found
    raise ValueError()


def _verify_arguments(given_args, expected_args):
    final_args = {}
    if len(given_args) != len(expected_args):
        raise ValueError()

    for given, expected in zip(given_args, expected_args):
        # make sure right type and matches allowed
        if expected.values and given not in expected.values:
            raise ValueError()
        try:
            fresh_clean_and_beautiful = _cast(given, expected.cast)
        except TypeError:
            raise ValueError()
        else:
            final_args[expected.key] = fresh_clean_and_beautiful
    return final_args


def _cast(value, t):
    if t == 'int':
        value = int(value)
    elif t == 'float':
        value = float(value)
    elif t == 'str':
        pass
    else:
        print(value, t)
        raise ValueError("This should have been verified already!")
    return value


def harvest(filepath, options=None):
    """Load a config file matching syntax against given options."""
    lines = []
    if not options: # must be in lang file
        options = _harvest_syntax(filepath)
        if not options: # still
            raise Exception("Language syntax not provided or found in file.")
    with open(filepath, 'r') as f:
        for raw_line in f:
            cmd, args = _split_input(raw_line)
            if not cmd:
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


def _help(allowed_syntaxes):
    indent = 0
    print(PREFIX + "Available Options:")
    indent += 4
    for i, (cmd, args) in enumerate(allowed_syntaxes):
        print(' '*indent, end='')
        print("[{}] {}".format(i, cmd.upper()), end='')
        for arg in args:
            if arg.values:
                print(" [{}]".format('|'.join(arg.values)), end='')
            else:
                print(" {}({})".format(arg.cast, arg.key), end='')
        print()
    indent -= 4


def _quit():
    print()
    raise SystemExit


def clear():
    os.system("cls" if os.name == "nt" else "clear")
