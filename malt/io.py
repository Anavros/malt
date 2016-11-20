
"""
Definitions of malt.offer() and malt.load().
Effectively compositions of lower-level parsing modules.
"""

from malt.objects import Response
from malt.exceptions import WrongType
from malt.parser import joiner, stripper, tokenizer, validator, finalizer
from malt.parser import signaturebuilder, responsebuilder


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
    tokens = tokenizer.tokenize(text)
    response = responsebuilder.build_response(tokens)
    signatures = signaturebuilder.generate_signatures(options)
    # TODO:
    # Error handling on unknown commands should probably be somewhere else.
    try:
        sig = signatures[response.head]
    except KeyError:
        # The given command doesn't match any known signature.
        print("KeyError: Unknown Command")
        return Response(None, {})
    else:
        combined = validator.validate(response, sig)
        try:
            return finalizer.finalize(combined)
        except WrongType:
            return Response(None, {})


def fantasy(text, options):
    if multiline:
        text = preprocess(text)

    userinput = structure(tokenize(text))
    signature = match_head(signatures, userinput)
    combined = match(userinput, signature)
    response = cast(combined)
    return response


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
