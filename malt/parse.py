
import re
import malt.cast as cast
from malt.exceptions import *

r_NEW_SYNTAX_LINE = r"""
^
(?P<head>[\w]+)
(?P<tail>\s+[\w\s|:=,.\[\]{}()+-]+)*
$
"""

r_NEW_SYNTAX_WORD = r"""
^
(?P<mod>[isfld])?
 (?(mod)(?P<lim>\([\w|:.]+\)))?
 (?(mod):)
(?P<key>[\w]+)
(?P<eq>=)?
 (?(eq)(?P<arg> [\w\s.:+-\[\]{}]+))
$
"""

r_NEW_INPUT_LINE = r"""
^
(?P<head>[\w/:]+)
(?P<tail>\s+[\w\s|:=,+-\[\]{}]+)*
$
"""

r_NEW_INPUT_WORD = r"""
^
(?P<key>[\w\s+-/:\[\]{}()]+)
(?P<eq>=)?
 (?(eq)(?P<arg> [\w\s+-/:{}\[\]()]+))
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
            spec = lim.strip('()') if lim is not None else ""
            if arg is not None:
                kwargs[key] = (arg, mod, spec)
            else:
                args.append((key, mod, spec))
        syntax[head] = args, kwargs
    return syntax


def parse_response(line):
    """
    Raises EmptyCommand, InputForbiddenCharacters.
    """
    if not line: raise EmptyCommand()
    line_match = re.fullmatch(r_NEW_INPUT_LINE, line, re.VERBOSE)
    if not line_match: raise InputForbiddenCharacters()
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
            raise InputForbiddenCharacters()
        key = word_match.group('key')
        arg = word_match.group('arg')
        if arg is not None:
            kwargs[key] = arg
        else:
            args.append(key)
    return head, args, kwargs


# BUG: silent error: key=value w/ unknown key
def validate(given, expected):
    """
    Compare the given input to the expected input. Returns the final dictionary containing
    every key:value pair from the response, typecasted and ready to use.
    
    Raises NotEnoughArgs, TooManyArgs, WrongType, and NotAnOption.
    """
    given_args, given_kwargs = given
    expec_args, expec_kwargs = expected
    final = {}

    # Verify argument counts.
    if   len(given_args) < len(expec_args): raise NotEnoughArgs()
    elif len(expec_args) < len(given_args): raise TooManyArgs()
    for given_arg, expec_arg in zip(given_args, expec_args):
        key, mod, lim = expec_arg
        value = given_arg
        final[key] = cast.auto(mod, value, lim)  # raises WrongType, NotAnOption

    # check for invalid keys
    for key in given_kwargs.keys():
        if key not in expec_kwargs.keys():
            raise UnknownKeyword()

    for key, params in expec_kwargs.items():
        (default, mod, lim) = params
        try:
            value = given_kwargs[key]
        except KeyError:
            value = default
        final[key] = cast.auto(mod, value, lim)  # raises WrongType, NotAnOption
    return final
