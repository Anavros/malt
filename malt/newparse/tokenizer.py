
from malt.newparse.constants import *

def get_tokens(contents):
    return parse(contents)

def parse(contents):
    state = ParserState()
    for c in contents:
        if c in WORD_SEPARATORS:
            state.tokenize_word(separator=c)
        elif c == QUOTE:
            state.in_quotes = not state.in_quotes
            state.word_buffer.append(c)
        elif c == LIST_BEGIN:
            if state.in_list:
                raise MaltSyntaxError("Nested list.")
            else:
               state.in_list = True
        elif c == DICT_BEGIN:
            if state.in_dict:
                raise MaltSyntaxError("Nested dict.")
            else:
               state.in_dict = True
        elif c == LIST_END:
            if not state.in_list:
                raise MaltSyntaxError("Ended list that never began.")
            else:
                state.tokenize_word()
                state.tokenize_list()
        elif c == DICT_END:
            if not state.in_dict:
                raise MaltSyntaxError("Ended dict that never began.")
            else:
                state.tokenize_word()
                state.tokenize_dict()
        else:
            state.word_buffer.append(c)
    return state.tokens


class MaltSyntaxError(ValueError):
    pass


class ParserState:
    def __init__(self):
        self.tokens = []
        self.word_buffer = []
        self.list_buffer = []
        self.dict_buffer = {}
        self.in_list = False
        self.in_dict = False
        self.in_quotes = False

    def tokenize_word(self, separator=' '):
        if self.word_buffer:
            if self.in_quotes:
                self.word_buffer.append(separator)
                return
            elif self.in_list:
                self.list_buffer.append(''.join(self.word_buffer))
            elif self.in_dict:  # overwrites if nested? shouldn't nest anyway
                # TODO: use second argument to split() to prevent this.
                if self.word_buffer.count(KEY_VALUE_JOIN) != 1:
                    raise MaltSyntaxError(
                        "Wrong number of ':' separators in line: {}".format(
                            self.word_buffer))
                i = self.word_buffer.index(KEY_VALUE_JOIN)
                k = ''.join(self.word_buffer[:i])
                v = ''.join(self.word_buffer[i+1:])
                self.dict_buffer[k] = v
            else:
                self.tokens.append(''.join(self.word_buffer))
                if separator == '=':
                    self.tokens.append('=')
                elif separator == '\n':
                    self.tokens.append(None)
            self.word_buffer = []
        else:
            # hacky
            if separator == '=':
                self.tokens.append('=')

    def tokenize_list(self):
        if self.list_buffer:
            self.tokens.append(self.list_buffer)
            self.list_buffer = []
        self.in_list = False
        self.tokens.append(None)

    def tokenize_dict(self):
        if self.dict_buffer:
            self.tokens.append(self.dict_buffer)
            self.dict_buffer = {}
        self.in_dict = False
        self.tokens.append(None)
