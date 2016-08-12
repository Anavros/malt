# coding=utf-8
"""
Malt
a tiny toolkit for making interactive loops
Output Extension
"""
from contextlib import contextmanager


def serve(output='', nl=True):
    """Print something to the console with smart formatting.

    Accepts one item at a time to print to the console. Items are checked by
    type and available attributes to determine the best way to format them.
    Generally speaking, output should be much more readable that the basic
    print function. Supports indentation.
    """
    if type(output) in [str, int, float]:
        _mprint(output, nl)

    # NOTE: nested tuples render as str(tuple)
    elif type(output) is tuple:
        if not output:
            _mprint('()')
        else:
            _mprint('(', nl=False)
            for item in output[:-1]:
                _mprint(str(item)+', ', nl=False)
            _mprint(str(output[-1]), nl=False)
            _mprint(')', nl)

    elif type(output) in [list, set, frozenset]:
        _mprint('[', nl=output)
        with indent():
            for i, item in enumerate(output):
                if not _fresh_line:
                    _mprint()
                #_mprint(LIST_TICK, nl=False)
                _mprint("[{}] ".format(i), nl=False)
                serve(item)
        _mprint(']', nl)

    elif type(output) is dict:
        _mprint("{", nl=output)
        with indent():
            for (key, value) in output.items():
                _mprint("{}: ".format(key), nl=False)
                serve(value)
        _mprint("}")

    # Helps with OrderedDict.
    elif hasattr(output, 'items'):
        serve(list(output.items()))

    # Stops objects like str from spewing everywhere.
    elif hasattr(output, '__dict__') and type(output.__dict__) is dict:
    #elif hasattr(output, '__dict__'):
        serve(output.__dict__, nl)

    elif hasattr(output, '_get_args()'):
        serve(list(output._get_args()))

    # When in doubt, use repr.
    else:
        _mprint(repr(output), nl)


@contextmanager
def indent():
    """Increase the indentation level for all output.

    Used with a context manager: 'with malt.indent(): ...'. Indentation levels
    are error-checked to prevent excessive or invalid levels. Client
    programmers do not need to error check use of this function. Set the
    malt.OVERFLOW global variable to set the maximum line width including
    indentation.
    """
    global _indent
    _indent = _indent+1
    try:
        yield
    finally:
        _indent = max(_indent-1, 0)


def confirm(prompt=PREFIX + "confirm? "):
    """Get a boolean yes or no from the console.

    Loops until a yes or no has been given. Does not accept unknown input to
    prevent accidental typing errors from causing problems.
    """
    while True:
        serve(prompt, nl=False)
        key = _minput().strip().lower()
        if key == 'yes':
            return True
        elif key == 'no':
            return False
        else:
            serve(PREFIX + "unknown keyword (use 'yes' or 'no')")
            serve()
            continue


def pause():
    """Pause for dramatic effect."""

    serve('...', nl=False)
    _minput()


def clear():
    """Clear the screen."""

    os.system("cls" if os.name == "nt" else "clear")


def line(char='=', insert=None):
    """Print a line of characters exactly as wide as the window."""

    if len(char) > 1:
        char = char[0]
    length = OVERFLOW-(min(_indent, MAX_INDENT) * INDENT_WIDTH)
    string = char*length
    if insert is not None:
        pass
    _mprint(string)


# XXX: doesn't maintain order any more
def explain(prototype, focus=None):
    """Serve a help message with all available commands."""
    with indent():
        if focus is not None:
            if focus in prototype.keys():
                serve(PREFIX + "Usage:")
                with indent():
                    serve(focus + ' ', nl=False)
                    args = prototype[focus]
                    for name, cast in args:
                        serve("[{} {}] ".format(str(cast)[8:-2], name), nl=False)
                    serve(nl=True)
            else:
                serve(PREFIX + "Unknown Command: '{}'".format(focus))
        else:
            serve(PREFIX + "Available Commands:")
            for command in prototype.keys():
                serve("'{}' ".format(command), nl=False)
            serve(nl=True)
            serve("'help', 'clear', 'back', and 'quit' are always available.")


def _mprint(string='', nl=True):
    """Print output to the console with extra functionality.

    Provides support for indentation and line truncation. Every call should go
    through _mprint() as it will ensure indentation will always be correct.
    """
    global _fresh_line, OVERFLOW
    global _indent, MAX_INDENT, INDENT_WIDTH
    already_printed = 0

    # Add indentation to the beginning of every new line.
    if _fresh_line:
        indentation = ' '*min(_indent, MAX_INDENT)*INDENT_WIDTH
        already_printed = len(indentation)
        print(indentation, end='')

    string = str(string)  # cast ints and anything else just to make sure
    end_char = '\n' if nl else ''

    # Wrap the line via recursion if it is too long.
    if already_printed + len(string) > OVERFLOW:
        remaining = OVERFLOW-already_printed
        cut = OVERFLOW  # not 0 to prevent infinite loops on long words
        # should get the whitespace closest to the maximum allowed length
        for i in range(remaining):
            if string[i].isspace():
                cut = i
        print(string[:cut], end='\n')
        _fresh_line = True
        _mprint(string[cut:].strip(), nl)
    else:
        print(string, end=end_char)

    # The next line will be 'fresh' if it follows a newline.
    _fresh_line = nl



def _minput():
    """Wrapper for input() to help provide indentation support."""
    global _fresh_line
    _fresh_line = True

    x = input()
    if x.strip().lower() == 'quit':
        raise SystemExit
    else:
        return x
