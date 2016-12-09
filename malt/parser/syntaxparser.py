
from malt.constants import EQUALS, SEPARATORS, JOIN, DOUBLE_QUOTE
from malt.constants import LIST_BEGIN, LIST_END, DICT_BEGIN, DICT_END
from malt.exceptions import MaltSyntaxError
from malt.objects import Argument, Signature


def parse(text):
    return build_response(tokenize(text))


# Does this not throw any errors?
# It's not externally callable, so maybe not?
def build_response(tokens):
    """
    Turn a line of tokens into a Response object.
    """
    head = ""
    body = []
    i = 0
    for token in tokens:
        # The first token always becomes the head.
        if not head:
            head = token
            continue

        # ex: 'key=value'
        if EQUALS in token:
            key, value = token.split(EQUALS, 1)
        else:
            # If a key is not provided, use the integer position of the arg.
            key, value = None, token

        body.append(Argument(i, key, value, None))
        i += 1
    return Signature(head, body)


# BUG: duplicate functionality with preprocessor.collapse_lists
def tokenize(stream):
    state = ParserState()
    for c in stream:
        if c in SEPARATORS:
            state.end_word(separator=c)
        elif c == DOUBLE_QUOTE:  # TODO: allow single quotes
            state.in_quotes = not state.in_quotes
            state.word_buffer.append(c)
        elif c == LIST_BEGIN:
            if state.in_list:
                raise MaltSyntaxError("nested list")
            else:
               state.in_list = True
        elif c == DICT_BEGIN:
            if state.in_dict:
                raise MaltSyntaxError("nested dict")
            else:
               state.in_dict = True
        elif c == LIST_END:
            if not state.in_list:
                raise MaltSyntaxError("ended list that never began")
            else:
                state.end_word()
                state.end_list()
        elif c == DICT_END:
            if not state.in_dict:
                raise MaltSyntaxError("ended dict that never began")
            else:
                state.end_word()
                state.end_dict()
        else:
            state.word_buffer.append(c)
    state.end_word()
    return state.tokens


class ParserState:
    def __init__(self):
        self.tokens = []
        self.word_buffer = []
        self.list_buffer = []
        self.dict_buffer = {}
        self.in_list = False
        self.in_dict = False
        self.in_quotes = False

    def end_word(self, separator=' '):
        if self.word_buffer:
            if self.in_quotes:
                self.word_buffer.append(separator)
                return

            elif self.in_list:
                self.list_buffer.append(''.join(self.word_buffer))

            elif self.in_dict:  # overwrites if nested? shouldn't nest anyway
                # TODO: use second argument to split() to prevent this.
                if self.word_buffer.count(JOIN) != 1:
                    raise MaltSyntaxError(
                        "Wrong number of ':' separators in line: {}".format(
                            self.word_buffer))
                i = self.word_buffer.index(JOIN)
                k = ''.join(self.word_buffer[:i])
                v = ''.join(self.word_buffer[i+1:])
                self.dict_buffer[k] = v

            else:
                self.tokens.append(''.join(self.word_buffer))
            self.word_buffer = []
        self.end_line(separator)

    def end_line(self, c):
        if c != '\n':
            return
        if self.in_list or self.in_dict or self.in_quotes:
            return
        else:
            self.tokens.append(None)

    def end_list(self):
        if self.list_buffer:
            self.tokens.append(self.list_buffer)
            self.list_buffer = []
        self.in_list = False

    def end_dict(self):
        if self.dict_buffer:
            self.tokens.append(self.dict_buffer)
            self.dict_buffer = {}
        self.in_dict = False
