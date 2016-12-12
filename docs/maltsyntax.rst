
Malt Syntax
***********

Whether reading a command in an interactive program or loading a config file,
malt expects a particular syntax for its input.

Every input must contain at least one word; the *head*. Empty lines are ignored.
Following the head is the *body*, zero or more space-separated arguments. Some
arguments are *positional* and some are *keyword*, as they are in python.
Positional arguments are expected in particular positions, unsurprisingly.
Keyword arguments can be placed anywhere after the positional arguments are
finished or omitted completely to use default values::

    command
    command posarg1 posarg2
    command posarg1 posarg2 kwarg1=val1 kwarg2=val2 kwarg3=val3
    command posarg1 posarg2 kwarg2=val2 kwarg1=val1

Lists are written as space-separated values within brackets. No commas are
required. Empty lists are written as two brackets with no contents::

    list [a b c d]
    list []

Dicts are similar: they are space-separated key:value pairs inside curly
braces.

Note that there must not be any space between the key and value!::

    dict {eggs:1 spam:2 sausage:3}
    dict {}
    dict {bad: "oh no"}  # don't put spaces between keys and values!

Multi-line config files loaded by ``malt.load`` have an additional preprocessor
step that enables two things: 1) comments and 2) line continuation::

    # Comments are marked with hash characters.

    example "file.malt"  # they can come inline too

    ###
    Lines marked with triple-hashes (and only three!) begin block comments.
    You can put whatever you want inside here.
    ###

    # Line continuations can happen implicitly or explicitly.
    # Finishing a line with three dots: ...
    # Will escape the newline and join that line with the following one.

    example ...
        "file.malt"

    # The indentation isn't important.

    # Implicit continuations happen inside lists and dicts:

    list [
        a
        b
        c
    ]

    dict {
        a:1
        b:2
        c:3
    }

    # No newline will count when contained within brackets.
    # Note that you still shouldn't put spaces between your k:v in dicts!

    dict {
        a: 1  # still causes problems, even in config files
    }
