
"""
Definitions of malt.offer() and malt.load().
Effectively compositions of lower-level parsing modules.
"""

from malt.objects import Response
from malt.exceptions import WrongType, MaltSyntaxError, MissingValue
from malt.exceptions import UnknownKeyword, UnknownCommand
from malt.parser import joiner, stripper, tokenizer, validator, finalizer
from malt.parser import signaturebuilder, responsebuilder, errorhandler
from malt.parser import matcher


def offer(options):
    try:
        text = input('> ')
    except (KeyboardInterrupt, EOFError):
        raise SystemExit # silent exit without stack trace
    else:
        return parse(text, options)


def parse(text, options):
    """
    Parse a single line of input.
    """
    try:
        tokens = tokenizer.tokenize(text)
    except MaltSyntaxError as e:
        return errorhandler.mock_response(e)

    # Throws no errors?
    # Assuming correct tokens.
    response = responsebuilder.build_response(tokens)

    try:
        signatures = signaturebuilder.generate_signatures(options)
    except EmptyOptionString as e:
        return errorhandler.mock_response(e)

    try:
        signature = matcher.find(response, signatures)
    except UnknownCommand as e:
        return errorhandler.mock_response(e)

    try:
        combined = validator.validate(response, signature)
    except (UnknownKeyword, MissingValue) as e:
        return errorhandler.mock_response(e)

    try:
        final = finalizer.finalize(combined)  # should be renamed to caster
    except WrongType as e:
        return errorhandler.mock_response(e)

    return final


def fantasy(text, options):
    pass


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
    # Raises errors if any problems are found.
    signaturebuilder.generate_signatures(options)
