
from malt.parser import preprocessor, tokenizer, matcher, caster
from malt.parser import responsebuilder, signaturebuilder, errorhandler


def preprocess(text):
    text = preprocessor.strip(text)
    text = preprocessor.continue_lines(text)
    text = preprocessor.collapse_lists(text)
    return text


def parse_options(options):
    available = signaturebuilder.generate_signatures(options)
    return available


def parse_user_input(text):
    tokens = tokenizer.tokenize(text)
    submitted = responsebuilder.build_response(tokens)
    return submitted


def match_command(submitted, available):
    expected = matcher.find(submitted, available)
    return expected


def match_arguments(userinput, signature):
    return matcher.match_arguments(userinput, signature)


def cast(complete):
    return caster.cast_arguments(complete)


def handle(error):
    return errorhandler.mock_response(error)
