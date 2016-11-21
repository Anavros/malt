

"""
Strips comments and whitespace from multi-line input strings.
Joins continued lines together and flattens multi-line lists and dicts.
"""

SPACES = ' \t'
COMMENTS = '#?'
MULTILINE_COMMENT = '###'

# TODO: better constant use
# TODO: malt-specific errors


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


# TODO: Include malt-specific errors.
def collapse_lists(filestring):
    joined_string = ""
    in_list = False
    in_dict = False
    for c in filestring:
        if c == '\n':
            if in_list or in_dict:
                joined_string += ' '
            else:
                joined_string += '\n'
        elif c in '[]{}':
            if c == '[':
                if in_list: raise ValueError()
                else: in_list = True
                joined_string += '['
            elif c == ']':
                if not in_list: raise ValueError()
                else: in_list = False
                joined_string += ']'
            elif c == '{':
                if in_dict: raise ValueError()
                else: in_dict = True
                joined_string += '{'
            elif c == '}':
                if not in_dict: raise ValueError()
                else: in_dict = False
                joined_string += '}'
        else:
            joined_string += c
    return joined_string


def continue_lines(filestring):
    joined = ""
    for line in filestring.split('\n'):
        if line[-3:] == '...':
            joined += line[:-3] + ' '
        else:
            joined += line + '\n'
    return joined
