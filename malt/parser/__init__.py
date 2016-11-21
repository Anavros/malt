
from malt.parser import preprocessor, optionparser, syntaxparser, matcher, caster
from malt.objects import Response


def preprocess(text):
    text = preprocessor.strip(text)
    text = preprocessor.continue_lines(text)
    text = preprocessor.collapse_lists(text)
    return text


def parse_options(options):
    return optionparser.parse_all(options)


def parse_user_input(text):
    return syntaxparser.parse(text)


def match_command(submitted, available):
    return matcher.find(submitted, available)


def match_arguments(userinput, signature):
    return matcher.match_arguments(userinput, signature)


def cast(complete):
    return caster.cast_arguments(complete)


def handle(error, silent=False):
    if not silent: print("[malt]", str(error))
    return Response("", {})
