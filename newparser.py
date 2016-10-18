
"""
Updated parser for malt.

Using real stateful parsing this time, and not just regex.
"""

# Special characters.
LIST_BEGIN = '['
LIST_END = ']'
DICT_BEGIN = '{'
DICT_END = '}'
LINE_CONTINUE = '...'
LINE_END = '\n'
COMMENT = '#'
MULTILINE_COMMENT = '###'
KEY_VALUE_JOIN = ':'
DEFAULT_ARG_SETTER = '='
EMPTY_DEFAULT_ARG = 'empty'
SYNTAX_HINT = '?'


def parse_file(path):
    f = open(path, 'r')
    in_comment = False
    for c in iter(lambda: f.read(1), ''):
        if c == COMMENT:
            in_comment = True
        elif c == LINE_END:
            in_comment = False
            print()
        if in_comment:
            print(c, end='')
        else:
            pass
    print('done!')

if __name__ == '__main__':
    parse_file("example.malt")
