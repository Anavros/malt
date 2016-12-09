
"""
Strips comments and whitespace from multi-line input strings.
Joins continued lines together and flattens multi-line lists and dicts.
"""

# TODO: streamline loops
# The entire file has to be iterated multiple times to preprocess.

from malt.constants import *
from malt.exceptions import *


def strip(filestring):
    """
    Remove comments from a newline-separated string.
    """
    clean = []
    # TODO: use a string instead of list to simplify
    commented = False
    for line in filestring.split(LINE_END):
        line = line.strip()

        # Remove empty lines.
        if len(line) < 1:
            continue

        # Everything between multiline comment markers is ignored.
        if line == BLOCK_COMMENT:
            commented = not commented
            continue

        if not commented:
            stripped = strip_inline_comments(line)
            if len(stripped) < 1:
                continue
            else:
                clean.append(stripped)

    return LINE_END.join(clean)


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
        if c == '\"':
            double_quoted = not double_quoted
        if not double_quoted and c in COMMENTS:
            break
        new_line += c
    return new_line.rstrip(SEPARATORS)


# TODO: Disallow lists in dicts and vice-versa.
def collapse_lists(filestring):
    joined_string = ""
    in_list = False
    in_dict = False
    for c in filestring:
        if c == LINE_END:
            if in_list or in_dict:
                joined_string += ' '
            else:
                joined_string += LINE_END
        elif c in BRACES:
            if c == LIST_BEGIN:
                if in_list: raise MaltSyntaxError("nested list")
                else: in_list = True
                joined_string += LIST_BEGIN
            elif c == LIST_END:
                if not in_list: raise MaltSyntaxError("mismatched list ending")
                else: in_list = False
                joined_string += LIST_END
            elif c == DICT_BEGIN:
                if in_dict: raise MaltSyntaxError("nested dict")
                else: in_dict = True
                joined_string += DICT_BEGIN
            elif c == DICT_END:
                if not in_dict: raise MaltSyntaxError("mismatched dict ending")
                else: in_dict = False
                joined_string += DICT_END
        else:
            joined_string += c
    return joined_string


def continue_lines(filestring):
    """
    Join lines that end with the continuation marker (default: '...').
    """
    joined = ""
    for line in filestring.split(LINE_END):
        if line[-3:] == LINE_CONTINUE:
            joined += line[:-3] + ' '
        else:
            joined += line + LINE_END
    return joined
