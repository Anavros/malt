
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
COMMENT = '#'
MULTILINE_COMMENT = '@'
KEY_VALUE_JOIN = ':'
DEFAULT_ARG_SETTER = '='
EMPTY_DEFAULT_ARG = 'empty'
SYNTAX_HINT = '?'

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


def preprocess(contents):
    """
    Remove comments from the file to make parsing easier.

    Return the gutted file as a string.
    """
    cleaned_contents = []
    in_multiline_comment = False
    for line in contents.split('\n'):
        if marks_multiline_comment(line):
            in_multiline_comment = not in_multiline_comment
            continue

        if in_multiline_comment:
            continue

        clean = strip_comments(line)
        if len(clean) > 0:
            cleaned_contents.append(clean)
    return cleaned_contents


def marks_multiline_comment(line):
    return (len(line) == 3) and (line[0:2] == '###')


def strip_comments(line):
    return line.split('#')[0]


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
    clean_lines = preprocess(load_file("example.malt"))
    for l in clean_lines:
        print(l)
    #parse_file("example.malt")
