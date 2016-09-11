
import re
import os
import shlex


"""Malt
A tiny toolkit for structured input and output.
"""

PREFIX = '[malt] '
PROMPT = '> '

r_SYNTAX_FORM = r"""
^
(?P<cast>(str|int|float))?  # Optional type cast: type(example).
 (?(cast) \( )              # Only matches paren if cast is matched.
(?P<key>[a-z]+)             # Required keyword.
 (?(cast) \) )              # Closing paren for cast.
(?P<allow>\[[\w\d_|]+\])?   # Optional list of allowed values.
$
"""

r_NEW_SYNTAX_LINE = r"""
^
(?P<head>[\w]+)
(?P<tail>\s+[\w\s|:=,\[\]]+)*
$
"""

r_NEW_SYNTAX_WORD = r"""
^
(?P<mod>[isf])?
 (?(mod)(?P<lim>\[[\w|]+\]))?
 (?(mod):)
(?P<key>[\w]+)
(?P<arg>=[\w]+)?
$
"""

### PUBLIC FUNCTIONS ###

def offer(options):
    """Offer the user a list of options. Input is verified as returned as a
    Response object."""

    # syntax -> ? add thing, i:n, pre=butt, i:mod=1
    # raw text -> add butt, 5, mod=1
    # head and tail -> add, (butt, 5, mod=1)
    # make sure head is valid
    # maybe built struct -> args=[], kwargs={}
    # make sure tail args are alright
    # typecast and verify args

    allowed_syntaxes = _compile(options)
    try:
        raw_text = input(PROMPT)
    except (KeyboardInterrupt, EOFError):
        quit()
    if not raw_text:
        return Response(None)

    head, tail = _match(raw_text)
    #assert head in options
    args = []
    kwargs = {}
    for word in tail.split(','):
        if '=' in word:
            k, v = word.split('=')
            kwargs[k] = v
        else:
            args.append(word)

    

    try:
        expected_args = _get_args(command, allowed_syntaxes)
    except ValueError:
        if command == 'help':
            help(allowed_syntaxes)
        elif command == 'clear':
            clear()
        elif command == 'quit':
            quit()
        else:
            print(PREFIX+"unknown command")
        return Response(None)

    try:
        final_args = _verify_arguments(given_args, expected_args)
    except ValueError:
        print(PREFIX+"malformed or missing arguments")
        return Response(None)
    else:
        return Response(command, final_args)


def load(filepath, options=None):
    """Load a config file matching syntax against given options."""
    if options:
        syntax = _parse(options)
    else:
        syntax = _read_syntax_comments(filepath)
        serve(syntax)
        input()
    responses = []
    with open(filepath, 'r') as f:
        for raw_line in f:
            line = raw_line.split('#')[0].strip()
            line = line.split('?')[0].strip()
            if not line: continue

            head, tail = _match(line)
            args, kwargs = _match_tail(tail)
            # check head
            #args = process(tail)
            #expected_args = _get_args(command, allowed_syntaxes)
            #final_args = _verify_arguments(words, expected_args)
            #responses.append(Response(head, tail))
            print("HEAD")
            serve(head)
            print("ARGS")
            serve(args)
            print("KWARGS")
            serve(kwargs)
    return responses


def serve(content='', end='\n', indent=0):
    """Prints easy-to-read data structures according to type."""
    if type(content) in [str, int, float]:
        print(content)
    elif type(content) in [list, set, frozenset, tuple]:
        indent += 4
        print('[')
        for i, item in enumerate(content):
            print(' '*indent, end='')
            print("[{}] ".format(i), end='')
            serve(item, indent=indent)
        indent -= 4
        print(' '*indent, end='')
        print(']')
    elif type(content) is dict:
        print('{')
        indent += 4
        for (key, value) in content.items():
            print(' '*indent, end='')
            print("{}: ".format(key), end='')
            serve(value, indent=indent)
        indent -= 4
        print(' '*indent, end='')
        print('}')
    # Helps with OrderedDict.
    elif hasattr(content, 'items'):
        serve(list(content.items()))
    # Stops objects like str from spewing everywhere.
    elif hasattr(content, '__dict__') and type(content.__dict__) is dict:
        serve(content.__dict__, end, indent=indent)
    elif hasattr(content, '_get_args()'):
        serve(list(content._get_args()), indent=indent)
    # When in doubt, use repr.
    else:
        print(repr(content), end=end)


def help(allowed_syntaxes):
    indent = 0
    print(PREFIX + "Available Options:")
    indent += 4
    for i, (cmd, args) in enumerate(allowed_syntaxes):
        print(' '*indent, end='')
        print("[{}] {}".format(i, cmd.upper()))
        indent += 4
        for arg in args:
            print(' '*indent, end='')
            if arg.values:
                print("* [{}]".format('|'.join(arg.values)))
            else:
                print("* {}({})".format(arg.cast, arg.key))
        indent -= 4
    indent -= 4


def quit():
    print()
    raise SystemExit


def clear():
    os.system("cls" if os.name == "nt" else "clear")

### INTERNAL FUNCTIONS ###

class Argument(object):
    def __init__(self, key, mod='str', lim=None, arg=None):
        self.key = key
        self.mod = mod
        self.lim = lim
        self.arg = arg


class Response(object):
    def __init__(self, cmd, args=None):
        self.cmd = cmd
        if args is not None:
            for k, v in args.items():
                self.__dict__[k] = v
    def __eq__(self, string):
        return self.cmd == string


def _read_syntax_comments(filepath):
    raw_lines = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line[0] != '?':
                continue
            raw_lines.append(line.strip('?').strip())
    if not raw_lines:
        raise ValueError("Malt syntax not provided or found in file.")
    return _parse(raw_lines)


def _parse(options):
    if not options: raise ValueError("Must provide a valid list of options!")
    if type(options) is str: options = [options]
    syntax = {}
    for line in options:
        head, tail = _match(line)
        syntax[head] = _match_tail(tail)
    return syntax


def _match(line):
    line_match = re.fullmatch(r_NEW_SYNTAX_LINE, line, re.VERBOSE)
    if not line_match:
        raise ValueError("Malformed syntax line:\n\t{}".format(line))
    head = line_match.group('head')
    tail = line_match.group('tail')
    return head, tail


def _match_tail(tail):
    args = []
    kwargs = {}
    for word in tail.split(','):
        word = word.strip()
        word_match = re.fullmatch(r_NEW_SYNTAX_WORD, word, re.VERBOSE)
        if not word_match:
            raise ValueError("Unmatched word: {}".format(word))
        key = word_match.group('key')
        mod = word_match.group('mod')
        lim = word_match.group('lim')
        arg = word_match.group('arg')
        obj = Argument(key, mod, lim, arg)
        if arg is not None:
            obj.arg = arg.strip('=')
            kwargs[key] = obj
        else:
            args.append(obj)
    return args, kwargs


def _get_args(user_cmd, allowed_syntaxes):
    for (cmd, args) in allowed_syntaxes:
        if user_cmd.lower() == cmd.lower():
            return args
    # if not found
    raise ValueError("{} was not found.".format(user_cmd))


def _verify_arguments(given_args, expected_args):
    final_args = {}
    if len(given_args) != len(expected_args):
        raise ValueError()
    for given, expected in zip(given_args, expected_args):
        # make sure right type and matches allowed
        if expected.values and (given not in expected.values):
            raise ValueError("Unexpected value '{}' found in limited arg.".format(given))
        try:
            fresh_clean_and_beautiful = _cast(given, expected.cast)
        except TypeError:
            raise ValueError("Failed to cast '{}' to type {}.".format(
                given, expected.cast))
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
