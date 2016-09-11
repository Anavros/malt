
import re
import os
import shlex


"""Malt
A tiny toolkit for structured input and output.
"""

PREFIX = '[malt] '
PROMPT = '> '

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
(?P<eq>=)?
 (?(eq)(?P<arg> [\w]+))
$
"""

r_NEW_INPUT_LINE = r"""
^
(?P<head>[\w]+)
(?P<tail>\s+[\w\s|:=,\[\]]+)*
$
"""

r_NEW_INPUT_WORD = r"""
^
(?P<key>[\w\s]+)
(?P<eq>=)?
 (?(eq)(?P<arg> [\w]+))
$
"""

### PUBLIC FUNCTIONS ###

def offer(options):
    """Offer the user a list of options. Input is verified as returned as a
    Response object."""
    syntax = _parse(options)

    try:
        raw_text = input(PROMPT)
    except (KeyboardInterrupt, EOFError):
        quit()
    if not raw_text:
        return Response(None, None)
    head, args, kwargs = _parse_response(raw_text)
    try:
        syn = syntax[head]
    except KeyError:
        print("Unknown key!")
        return Response(None, None)
    try:
        body = _validate((args, kwargs), syn)
    except ValueError:
        print("Bad typing!")
        return Response(None, None)
    return Response(head, body)


def load(filepath, options=None):
    """Load a config file matching syntax against given options."""
    if options:
        syntax = _parse(options)
    else:
        syntax = _parse(_syntax_hints(filepath))
    responses = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.split('#')[0].strip()
            line = line.split('?')[0].strip()
            if not line: continue

            head, raw_args, raw_kwargs = _parse_response(line)
            body = _validate((raw_args, raw_kwargs), syntax[head])

            print("SYNTAX")
            serve(syntax)
            print("HEAD")
            serve(head)
            print("BODY")
            serve(body)
            responses.append(Response(head, body))
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

class Response:
    def __init__(self, head, body):
        self.head = head
        if body is not None:
            for k, v in body.items():
                self.__dict__[k] = v
    def __eq__(self, x):
        return self.head == x


def _syntax_hints(filepath):
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
    return raw_lines


def _parse(options):
    if not options: raise ValueError("Must provide a valid list of options!")
    if type(options) is str: options = [options]
    syntax = {}
    for line in options:
        #head, args, kwargs = _match(line)
        line_match = re.fullmatch(r_NEW_SYNTAX_LINE, line, re.VERBOSE)
        if not line_match:
            raise ValueError("Malformed syntax line:\n\t{}".format(line))
        head = line_match.group('head')
        tail = line_match.group('tail')
        args = []
        kwargs = {}
        if not tail:
            syntax[head] = args, kwargs
            continue
        for word in tail.split(','):
            word = word.strip()
            word_match = re.fullmatch(r_NEW_SYNTAX_WORD, word, re.VERBOSE)
            if not word_match:
                raise ValueError("Unmatched word: {}".format(word))
            key = word_match.group('key')
            mod = word_match.group('mod')
            lim = word_match.group('lim')
            arg = word_match.group('arg')
            if arg is not None:
                kwargs[key] = (arg, mod, lim)
            else:
                args.append((key, mod, lim))
        syntax[head] = args, kwargs
    return syntax


def _parse_response(line):
    line_match = re.fullmatch(r_NEW_INPUT_LINE, line, re.VERBOSE)
    if not line_match:
        raise ValueError("Malformed input line:\n\t{}".format(line))
    head = line_match.group('head')
    tail = line_match.group('tail')
    args = []
    kwargs = {}
    if not tail:
        return head, args, kwargs
    for word in tail.split(','):
        word = word.strip()
        word_match = re.fullmatch(r_NEW_INPUT_WORD, word, re.VERBOSE)
        if not word_match:
            raise ValueError("Unmatched word: {}".format(word))
        key = word_match.group('key')
        arg = word_match.group('arg')
        if arg is not None:
            kwargs[key] = arg
        else:
            args.append(key)
    return head, args, kwargs


def _validate(given, expected):
    given_args, given_kwargs = given
    expec_args, expec_kwargs = expected
    final = {}

    if len(given_args) < len(expec_args):
        raise ValueError("Missing positional arguments.")
    elif len(expec_args) < len(given_args):
        raise ValueError("Too many positional arguments.")
    for given_arg, expec_arg in zip(given_args, expec_args):
        key, mod, lim = expec_arg
        value = given_arg
        final[key] = _cast(value, mod, lim)  # raises TypeError

    for key, params in expec_kwargs.items():
        (default, mod, lim) = params
        try:
            value = given_kwargs[key]
        except KeyError:
            value = default
        final[key] = _cast(value, mod, lim)  # raises TypeError
    return final


def _cast(value, mod, lim=None):
    if mod == 'i':
        value = int(value)
    elif mod == 'f':
        value = float(value)
    elif mod == 's':
        if lim is not None and value not in lim:
            raise TypeError("Expected value {} to be one of: {}".format(value, lim))
        pass
    elif mod is None:
        pass
    else:
        print(value, mod)
        raise ValueError("This should have been verified already!")
    return value
