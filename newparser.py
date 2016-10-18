
"""
Updated parser for malt.

Using real stateful parsing this time, not just regex.
"""

# Special characters.
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
SPACES = ' \t'


def load_file(path):
    f = open(path, 'r')
    return f.read()


# Tokens.
class Tokens:
    WORD, LIST, DICT= range(3)


class MaltSyntaxError(ValueError):
    pass


class ParserState:
    def __init__(self):
        self.word_buffer = []
        self.list_buffer = []
        self.dict_buffer = {}
        self.tokens = []
        self.in_list = False
        self.in_dict = False
        self.new_line = True

    def add_word(self):
        if self.word_buffer:
            self.tokens.append(''.join(self.word_buffer))
        else:
            pass  # Don't add empty tokens.

WORD_SEPARATORS = [' ', '\t', '\n']

def parse(contents):
    state = ParserState()
    for c in contents:
        if c in WORD_SEPARATORS:
            if not state.word_buffer:
                continue
            if state.in_list:
                state.list_buffer.append(''.join(state.word_buffer))
            elif state.in_dict:
                if state.word_buffer.count(KEY_VALUE_JOIN) != 1:
                    raise MaltSyntaxError("Missing key:value separator or:too:many.")
                i = state.word_buffer.index(KEY_VALUE_JOIN)
                k = ''.join(state.word_buffer[:i])
                v = ''.join(state.word_buffer[i:])
                state.dict_buffer[k] = v
            else:
                state.tokens.append(''.join(state.word_buffer))
                if c == '\n':
                    state.tokens.append(None)
            state.word_buffer = []

        elif c == LIST_BEGIN:
            if state.in_list:
                raise MaltSyntaxError("Nested list.")
            else:
               state.in_list = True

        elif c == LIST_END:
            if not state.in_list:
                raise MaltSyntaxError("Ended list that never began.")
            else:
                state.in_list = False
                if state.word_buffer:
                    state.list_buffer.append(''.join(state.word_buffer))
                    state.word_buffer = []
                if state.list_buffer:
                    state.tokens.append(state.list_buffer)
                    state.list_buffer = []
                state.tokens.append(None)

        elif c == DICT_BEGIN:
            if state.in_dict:
                raise MaltSyntaxError("Nested dict.")
            else:
               state.in_dict = True

        elif c == DICT_END:
            if not state.in_dict:
                raise MaltSyntaxError("Ended dict that never began.")
            else:
                state.in_dict = False
                if state.word_buffer:
                    if state.word_buffer.count(KEY_VALUE_JOIN) != 1:
                        raise MaltSyntaxError("Missing key:value separator or:too:many.")
                    i = state.word_buffer.index(KEY_VALUE_JOIN)
                    k = ''.join(state.word_buffer[:i])
                    v = ''.join(state.word_buffer[i:])
                    state.dict_buffer[k] = v
                    state.word_buffer = []
                if state.dict_buffer:
                    state.tokens.append(state.dict_buffer)
                    state.dict_buffer = {}
                state.tokens.append(None)

        else:
            state.word_buffer.append(c)
    return state.tokens



def preprocess(old_contents):
    """
    """
    new_contents = ""
    in_multiline_comment = False
    for line in old_contents.split(LINE_END):
        if marks_multiline_comment(line):
            in_multiline_comment = not in_multiline_comment
        if in_multiline_comment:
            continue
        if is_signature_hint(line):
            continue
        line = strip_inline_comments(line)
        if is_empty(line):
            continue
        if is_continued(line):
            new_contents += strip_continuation(line)
        else:
            new_contents += line + '\n'
    return new_contents


def is_continued(line):
    return len(line) >= 3 and line[-3:] == LINE_CONTINUE


def is_empty(line):
    return not line.strip(SPACES)


def marks_multiline_comment(line):
    return len(line) == 3 and line[0:3] == COMMENT*3


def strip_inline_comments(line):
    return line.split(COMMENT)[0].strip()


def is_signature_hint(line):
    return len(line) >= 1 and line[0] == SIGNATURE_HINT


def strip_continuation(line):
    return line.replace('...', '')


def read(state):
    pass

if __name__ == '__main__':
    content = preprocess(load_file("example.malt"))
    print("PREPROCESSOR")
    print(content)
    print("TOKENIZER")
    tokens = parse(content)
    for t in tokens:
        if t is None:
            print('='*10)
        else:
            print(t)
    #parse_file("example.malt")
