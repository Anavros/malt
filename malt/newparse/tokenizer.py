
LIST_BEGIN = '['
LIST_END = ']'
DICT_BEGIN = '{'
DICT_END = '}'
LINE_CONTINUE = '...'
LINE_END = '\n'
KEY_VALUE_JOIN = ':'
DEFAULT_ARG_SETTER = '='
EMPTY_DEFAULT_ARG = 'empty'
SIGNATURE_HINT = '?'

# For the comment remover.
COMMENT = '#'
QUOTE = '\"'
SPACES = ' \t'


def get_tokens(contents):
    return parse(contents)


WORD_SEPARATORS = [' ', '\t', '\n']

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
                if self.word_buffer.count(KEY_VALUE_JOIN) != 1:
                    raise MaltSyntaxError("Missing key:value separator or:too:many.")
                i = self.word_buffer.index(KEY_VALUE_JOIN)
                k = ''.join(self.word_buffer[:i])
                v = ''.join(self.word_buffer[i+1:])
                self.dict_buffer[k] = v
            else:
                self.tokens.append(''.join(self.word_buffer))
                if separator == '\n': self.tokens.append(None)
            self.word_buffer = []

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
