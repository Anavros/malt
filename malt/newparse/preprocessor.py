
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


# Signature hints are normally removed in preprocess().
def get_signature_hints(contents):
    """
    Get a list of every signature line in the file.
    Signature hints define the parameters for commands in the same file. They are
    special comments and are normally removed in preprocessing.

    >>> file_content = '''
    ... ? add i:x i:y
    ... add 3 1
    ... add 6 10
    ... '''
    >>> get_signature_hints(file_content)
    ['? add i:x i:y']
    """
    signatures = []
    for line in contents.split(LINE_END):
        if is_signature_hint(line):
            signatures.append(line.strip())
    return signatures


def preprocess(old_contents):
    """
    Removes comments and signature lines from the raw file. Also joins lines ending
    with the continuation mark: '...'.

    >>> file_content = '''
    ...     ###
    ...     The preprocessor is responsible for removing comments and joining lines!
    ...     ###
    ...
    ...     config something setting 2  # inline comments are removed!
    ...
    ...     # Signature hints count as comments! They are removed as well.
    ...     ? config s:id |setting|tweak|quirk|:type i:n_tiles
    ...
    ...     # Any line (except for comments) ending in ...
    ...     # ...will be joined together!
    ...     config ...
    ...     another_thing quirk ...
    ...     5
    ...
    ...     # Also, everything here is indented! Unimportant whitespace is stripped.
    ...     '''
    >>> preprocess(file_content)
    'config something setting 2\\nconfig another_thing quirk 5\\n'
    """
    new_contents = ""
    in_multiline_comment = False
    for line in old_contents.split(LINE_END):
        line = line.strip()
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
            new_contents += line.rstrip() + LINE_END
    return new_contents


def is_continued(line):
    """
    Does this line end in the continuation mark '...'?
    >>> is_continued('command arg_one arg_two')
    False
    >>> is_continued('command arg_one ...')
    True
    """
    return len(line) >= 3 and line[-3:] == LINE_CONTINUE


def strip_continuation(line):
    """
    Remove the continuation mark after lines have been joined.
    >>> strip_continuation('command arg_one ...arg_two')
    'command arg_one arg_two'
    """
    return line.replace('...', '')


def is_empty(line):
    """
    >>> is_empty('hello there')
    False
    >>> is_empty('')
    True
    >>> is_empty('\t\t        ')
    True
    """
    return not line.strip(SPACES)


def marks_multiline_comment(line):
    """
    Does this line begin or end a multiline comment?
    Multiline comments are marked with '###'. The line may only contain those chars.
    >>> marks_multiline_comment('nothing to see here')
    False
    >>> marks_multiline_comment('###')
    True

    Whitespace IS important here. There must be no space before or after.
    >>> marks_multiline_comment('  ###  ')
    False
    """
    return len(line) == 3 and line[0:3] == COMMENT*3


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
        if c == QUOTE:
            double_quoted = not double_quoted
        if not double_quoted and c == COMMENT:
            break
        new_line += c
    return new_line.rstrip(SPACES)


def is_signature_hint(line):
    """
    Signature hints are comments that start with a question mark: '?'. They are
    used to define the syntax of commands in the same file.

    >>> is_signature_hint('not a signature hint')
    False
    >>> is_signature_hint('# close, but no cigar')
    False
    >>> is_signature_hint('? command s:string_arg i:int_arg')
    True

    Leading whitespace is ignored.
    >>> is_signature_hint('    ? command s:string_arg i:int_arg')
    True
    """
    line = line.strip()
    return len(line) >= 1 and line[0] == SIGNATURE_HINT
