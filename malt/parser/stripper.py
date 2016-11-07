

"""
Strips comments and whitespace from multi-line input strings.
"""

COMMENTS = '#?'
MULTILINE_COMMENT = '###'


def strip(filestring):
    clean = []
    commented = False
    for line in filestring.split('\n'):
        line = line.strip()
        # Remove empty lines.
        if not line:
            continue
        # Toggle the 'commented' bool if a multi-line comment marker is found.
        if line.strip() == MULTILINE_COMMENT:
            commented = not commented
            continue
        # ...
        if not commented:
            if line[0] not in COMMENTS:
                clean.append(strip_inline_comments(line))
            else:
                continue
    return '\n'.join(clean)


# TODO: Could use some polish, use constants instead of characters.
# TODO: Allow single quotes and literal characters.
def strip_inline_comments(line):
    """
    Removes comments that follow normal lines. Will ignore comment characters if they
    are in quotes. Currently there is no way to escape quotes if you want the raw chars.

    >>> strip_inline_comments('combine [these things]  # this is a list of strings!')
    'combine [these things]'

    >>> strip_inline_comments('lines may contain \"#\"hashes if double quoted!')
    'lines may contain \"#\"hashes if double quoted!'

    >>> strip_inline_comments('but #only in quotes! for obvious reasons')
    'but'

    >>> strip_inline_comments('do it\t   # Trailing whitespace is stripped too!')
    'do it'
    """
    new_line = ""
    double_quoted = False
    for c in line:
        if c == '"':
            double_quoted = not double_quoted
        if not double_quoted and c == '#':
            break
        new_line += c
    return new_line.rstrip(' \t')
