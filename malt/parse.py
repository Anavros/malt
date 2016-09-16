
import re

r_NEW_SYNTAX_LINE = r"""
^
(?P<head>[\w]+)
(?P<tail>\s+[\w\s|:=,.\[\]{}]+)*
$
"""

r_NEW_SYNTAX_WORD = r"""
^
(?P<mod>[isfld])?
 (?(mod)(?P<lim>\[[\w|]+\]))?
 (?(mod):)
(?P<key>[\w]+)
(?P<eq>=)?
 (?(eq)(?P<arg> [\w\s.+-\[\]{}]+))
$
"""

r_NEW_INPUT_LINE = r"""
^
(?P<head>[\w]+)
(?P<tail>\s+[\w\s|:=,+-\[\]{}]+)*
$
"""

r_NEW_INPUT_WORD = r"""
^
(?P<key>[\w\s+-/:]+)
(?P<eq>=)?
 (?(eq)(?P<arg> [\w\s+-/:{}\[\]]+))
$
"""

def syntax_hints(filepath):
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


def parse(options):
    if not options: raise ValueError("Must provide a valid list of options!")
    if type(options) is str: options = [options]
    syntax = {}
    for line in options:
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
                raise ValueError("Unmatched word in syntax: {}".format(word))
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


def parse_response(line):
    line_match = re.fullmatch(r_NEW_INPUT_LINE, line, re.VERBOSE)
    if not line_match:
        raise ValueError("forbidden characters in input")
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
            raise ValueError("misformatted argument")
        key = word_match.group('key')
        arg = word_match.group('arg')
        if arg is not None:
            kwargs[key] = arg
        else:
            args.append(key)
    return head, args, kwargs


def validate(given, expected):
    given_args, given_kwargs = given
    expec_args, expec_kwargs = expected
    final = {}

    if len(given_args) < len(expec_args):
        raise ValueError("missing positional arguments (expected {})".format(
            len(expec_args)))
    elif len(expec_args) < len(given_args):
        raise ValueError("too many positional arguments (expected {})".format(
            len(expec_args)))
    for given_arg, expec_arg in zip(given_args, expec_args):
        key, mod, lim = expec_arg
        value = given_arg
        final[key] = cast(value, mod, lim)  # raises TypeError

    for key, params in expec_kwargs.items():
        (default, mod, lim) = params
        try:
            value = given_kwargs[key]
        except KeyError:
            value = default
        final[key] = cast(value, mod, lim)  # raises TypeError
    return final


def cast(value, mod, lim=None):
    if mod == 'i':
        value = int(value)
    elif mod == 'f':
        value = float(value)
    elif mod == 's':
        if lim is not None and value not in lim:
            raise TypeError("Expected value {} to be one of: {}".format(value, lim))
        pass
    elif mod == 'd':
        # d:dict={1:one 2:two}
        # dict=1:one 2:two, {1:one, 2:two}
        pairs = [s.split(':') for s in value.strip('{}').split()]
        if not pairs:
            print("empty dict!")
            value = {}
        else:
            value = {k:v for k, v in pairs}
    elif mod == 'l':
        # l:list=[1 2 3] -> [1, 2, 3]
        # [1 2 3], 1 2 3, list=1 2 3, 
        value = list(value.strip('[]').split())
    elif mod is None:
        pass
    else:
        raise ValueError("Invalid type parameter! Type: {}".format(mod))
    return value
