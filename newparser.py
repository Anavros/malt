
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
        self.buffer = []
        self.tokens = []
        self.in_list = False
        self.in_dict = False
        self.new_line = True


def parse(contents):
    state = ParserState()
    for c in contents:
        if c == ' ':
            if state.in_list or state.in_dict:
                continue
            state.tokens.append((Tokens.WORD, ''.join(state.buffer)))
            state.buffer = []
        elif c == LINE_END:
            if state.in_list or state.in_dict:
                continue
            state.tokens.append((Tokens.WORD, ''.join(state.buffer)))
            state.buffer = []
        elif c == LIST_BEGIN:
            # NOTE: no nested lists
            if state.in_list:
                raise MaltSyntaxError("Nested list.")
            else:
               state.in_list = True
        elif c == LIST_END:
            if not state.in_list:
                raise MaltSyntaxError("Ended list that never began.")
            else:
                state.in_list = False
                state.tokens.append((Tokens.LIST, ''.join(state.buffer)))
                state.buffer = []
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
                state.tokens.append((Tokens.DICT, ''.join(state.buffer)))
                state.buffer = []
        else:
            state.buffer.append(c)
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
    return len(line) == 3 and line[0:2] == COMMENT*3


def strip_inline_comments(line):
    return line.split(COMMENT)[0].strip()


def is_signature_hint(line):
    return len(line) >= 1 and line[0] == SIGNATURE_HINT


def strip_continuation(line):
    return line.replace('...', '')


def read(state):
    pass

if __name__ == '__main__':
    print(parse(preprocess(load_file("example.malt"))))
    #parse_file("example.malt")
