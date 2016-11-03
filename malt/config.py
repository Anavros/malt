
"""
User-configurable options.
"""

AUTOCLEAR = False
"""
Enable a nicer interface that keeps the user prompt at the bottom of the term.
Only use for interactive sessions.
"""

#TAB_WIDTH = 4
tab_width = 4
"""
The number of spaces to insert for each indentation level.
"""

PROMPT = '> '
"""
A short string to be printed before every user input.
"""

PREFIX = '[malt] '
"""
Printed before error messages and other malt-related things.
"""

N_LINES = 100
"""
An arbitrary number of lines meant to be larger than the number of rows in
the terminal. Used for clearing the screen with newline spam.
"""

RECURSION_LIMIT = 5

# ADD: Formatting options, like which brackets to use, etc.
# Could be merged with the new parser constants too.
