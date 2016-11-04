

"""
Strips comments and whitespace from multi-line input strings.
"""

COMMENTS = '#?'


def strip(filestring):
    dirty = filestring.split('\n')
    clean = []
    for line in dirty:
        line = strip_single_line_comments(line)
        clean.append(line)
    return clean


def strip_single_line_comments(line):
    return line
