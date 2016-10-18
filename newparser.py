
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

# Tokens.
class Tokens:
    COMMENT, MULTICOMMENT, LIST, DICT = range(4)


class ParserState:
    def __init__(self):
        self.in_comment = False
        self.in_multi_comment = False
        self.in_list = False
        self.in_dict = False
        self.new_line = True
        self.continue_line = False
        self.empty_line = True
        self.last_char = ''


def load_file(path):
    f = open(path, 'r')
    return f.read()


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


def parse(contents):
    state = ParserState()
    for c in contents:
        if c == ' ' or c == '\t':
            send_nothing(state)
        elif c == '\n':
            send_newline(state)
        else:
            send_char(state, c)
        read(state)


def send_nothing(state):
    state.last_char = ''


def send_newline(state):
    state.last_char = ''
    if state.continue_line:
        pass
    else:
        state.new_line = True
        state.empty_line = True
        state.in_comment = False


def send_char(state, c):
    state.new_line = False
    state.empty_line = False
    # Single-line comments.
    if c == COMMENT:
        state.in_comment = True

    # Multi-line comments.
    elif c == MULTILINE_COMMENT:
        if not state.in_comment:
            if state.in_multi_comment:
                state.in_multi_comment = False
            else:
                state.in_multi_comment = True

    state.last_char = c


def read(state):
    if not (state.in_comment or state.in_multi_comment):
        print(state.last_char, end='')

if __name__ == '__main__':
    print(preprocess(load_file("example.malt")))
    #parse_file("example.malt")
