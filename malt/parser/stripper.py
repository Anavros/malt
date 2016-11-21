

"""
Strips comments and whitespace from multi-line input strings.
"""

SPACES = ' \t'
COMMENTS = '#?'
MULTILINE_COMMENT = '###'


def strip(filestring):
    clean = []
    commented = False
    for line in filestring.split('\n'):
        line = line.strip()

        # Remove empty lines.
        if len(line) < 1:
            continue

        # Everything between multiline comment markers is ignored.
        if line == MULTILINE_COMMENT:
            commented = not commented
            continue

        if not commented:
            stripped = strip_inline_comments(line)
            if len(stripped) < 1:
                continue
            else:
                clean.append(stripped)

    return '\n'.join(clean)


# TODO: Allow single quotes and literal characters.
# TODO: Allow backslashed comments and quotes.
def strip_inline_comments(line):
    """
    Removes comments that follow normal lines. Will ignore comment characters
    if they are in quotes. Currently there is no way to escape quotes if you
    want the raw chars.
    """
    new_line = ""
    double_quoted = False
    for c in line:
        if c == '"':  # that's a " inside two '
            double_quoted = not double_quoted
        if not double_quoted and c in COMMENTS:
            break
        new_line += c
    return new_line.rstrip(SPACES)
