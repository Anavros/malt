
"""
Definitions of malt.offer() and malt.load().
Effectively compositions of lower-level parsing modules.
"""

from malt import preprocessor, tokenizer, compiler, validator


def offer(options):
    try:
        text = input('> ')
    except (KeyboardInterrupt, EOFError):
        raise SystemExit
    else:
        return parse(text, options)


def parse(text, options):
    """
    Parse a single line of input.
    """
    return validator.validate(compiler.compile(tokenizer.tokenize(text)))


def read(lines, options):
    return [parse(line, options) for line in lines]


def load(filepath, options):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    return read(lines, options)


def check_syntax(options):
    """
    Optional function to verify a given option list is usable.
    """
