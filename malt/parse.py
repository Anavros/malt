
import re
from malt.exceptions import *

r_NEW_SYNTAX_LINE = r"""
^
(?P<head>[\w]+)
(?P<tail>\s+[\w\s|:=,.\[\]{}()+-]+)*
$
"""

r_NEW_SYNTAX_WORD = r"""
^
(?P<mod>[isfldo])?
 (?(mod)(?P<lim>\([\w|-]+\)))?
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


# silent error: key=value w/ unknown key
def validate(given, expected):
    given_args, given_kwargs = given
    expec_args, expec_kwargs = expected
    final = {}

    # Verify argument counts.
    if   len(given_args) < len(expec_args): raise NotEnoughArgs()
    elif len(expec_args) < len(given_args): raise TooManyArgs()
    for given_arg, expec_arg in zip(given_args, expec_args):
        key, mod, lim = expec_arg
        value = given_arg
        final[key] = cast(value, mod, lim)  # raises WrongType, NotAnOption

    for key, params in expec_kwargs.items():
        (default, mod, lim) = params
        try:
            value = given_kwargs[key]
        except KeyError:
            value = default
        final[key] = cast(value, mod, lim)  # raises WrongType, NotAnOption
    return final


def cast(value, mod, specifics=""):
    print('specifics', specifics)

    # Integers
    if mod == 'i':
        try:
            value = int(value)
        except TypeError:
            raise WrongType()

        if specifics:
            ints = specifics.strip('()').split('-') # silent error
            low, high = int(ints[0]), int(ints[1])
            print(low, high)
            if low <= value <= high:
                print("matches!")
                return value
            else:
                print("no match")
                raise NotAnOption()
        else:
            return value

    # Floats
    elif mod == 'f':
        try:
            value = float(value)
        except TypeError:
            raise WrongType()
        else:
            return value

    # Strings
    elif mod == 's':
        return value

    # Dictionaries
    elif mod == 'd':
        # d:dict={1:one 2:two}
        # dict=1:one 2:two, {1:one, 2:two}
        pairs = [s.split(':') for s in value.strip('{}').split()]
        if not pairs:
            #print("empty dict!")
            return {}
        else:
            return {k:v for k, v in pairs}

    # Lists
    elif mod == 'l':
        # l:list=[1 2 3] -> [1, 2, 3]
        # [1 2 3], 1 2 3, list=1 2 3, 
        return list(value.strip('[]').split())

    # Limited Options
    elif mod == 'o':
        options = specifics.strip('()').split('|')
        if value in options:
            return value
        else:
            raise NotAnOption()

    # Default, assumes string
    elif mod is None:
        return value

    # Should have been one of those, regex error
    else:
        raise UnexpectedProgrammingError()
