
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
QUOTE = '\"'
SPACES = ' \t'


def strip_comments(contents):
    return preprocess(contents)


def join_continued_lines(contents):
    return contents


# Signature hints are normally removed in strip_comments().
def get_signature_hints(contents):
    pass


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
    new_line = ""
    double_quoted = False
    for c in line:
        if c == QUOTE:
            double_quoted = not double_quoted
        if not double_quoted and c == COMMENT:
            break
        new_line += c
    return new_line


def is_signature_hint(line):
    return len(line) >= 1 and line[0] == SIGNATURE_HINT


def strip_continuation(line):
    return line.replace('...', '')
