
from malt.constants import *
from malt.exceptions import MaltSyntaxError
from malt.objects import Argument, Signature


def parse(text):
    return Signature()


class Token:
    def __init__(self, key, value):
        self.key = key
        self.val = val


class Buffer:
    def __init__(self):
        pass


class ParsingState:
    def __init__(self):
        self.in_list = False
        self.in_dict = False
        self.in_single_quotes = False
        self.in_double_quotes = False

    def begin_list(self):
        if self.in_list: raise MaltSyntaxError("nested list")
        else: self.in_list = True


def tokenize(line):
    """
    Separate one line into string tokens.
    """
    tokens = []
    state = ParsingState()
    word_buffer = ""
    list_buffer = []
    dict_buffer = {}
    for c in line:
        if c in SEPARATORS:
            pass
        elif c in QUOTES:
            pass
        elif c in BRACES:
            if   c == LIST_BEGIN: state.begin_list()
            elif c == LIST_END: state.end_list()
            elif c == DICT_BEGIN: state.begin_dict()
            elif c == DICT_END: state.end_dict()
        else:
            word_buffer.append(c)
    return tokens


def convert(tokens):
    """
    Turn a list of tokens into a signature.
    """
    try:
        head = tokens.pop(0)
    except IndexError:
        return Signature("", [])

    body = []
    for i, token in enumerate(tokens):
        # ex: 'key=value'
        # What about turning lists into lists and etc?
        if EQUALS in token:
            key, value = token.split(EQUALS, 1)
        else:
            key, value = None, token

        body.append(Argument(i, key, value, None))
    return Signature(head, body)
