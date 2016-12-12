
Option String Syntax
********************

Malt uses specially-formatted *option strings* to parse input. Strings are easy
to use and terse, which is important when prototyping new interfaces. Each
public malt function, ``offer``, ``parse``, ``read``, and ``load`` takes a list
of one or more option strings. This guide will explain the option syntax.

Each option string must start with one word, referred to as the *head*. The head
can contain any characters not in ``:[]{}-=``; these are special characters used
for annotating arguments, which will come after the head::

    # All valid options.
    options = [
        "head",
        "command",
        "a",
        "/kick",
        "+",
    ]

Following the head is the *body*, a list of space-separated arguments that can
be annotated with types and default values. The argument syntax is::

    "typestring:name=value"

Both the typestring and value can be omitted. If there is no typestring, the
type will be considered ``s``; a string; i.e. no casting will be applied and
malt will return the argument unchanged from the user. If there is no default
value, the argument will be considered *positional* instead of *keyword*, and
the user will be required to enter a value for it.

There are currently six typestrings::

    "s:string"  -> No casting will be done. This is the default behavior.
    "i:int"     -> Input will be cast using int().
    "f:float"   -> Same using float().
    "b:bool"    -> False if input is '0' or 'False' (any case); otherwise True.

Two typestrings are compounds: lists and dicts. These are a little different.
Lists are marked as one basic type in brackets::

    "[i]:list_of_ints"

Dicts are similar, but with two values, separated by a dash::

    "{i-b}:map_of_ints_to_bools"

Note: probably could change that dash to a comma.

Lists and dicts will recursively cast their contents to the type specified
within the brackets. So ``[i]`` will create a list of ints, ``{i-s}`` will
create a dict of ints mapped to strings, and so on. If the internal cast is
omitted, it will default to ``s``, i.e. no cast::

    options = [
        "[s]:list_of_unchanged_strings",
        "[]:also_list_of_unchanged_strings",
        "{s-s}:dict_of_strings_to_strings",
        "{}:also_dict_of_strings_to_strings",
    ]

Bringing it all together::

    options = [
        "quit",
        "/ban",
        "/+/",
        "concat string1 string2",
        "add i:int1 i:int2",
        "sum [i]:numbers",
        "record {s-i}:phone_numbers",
        "associate {}:string_mappings",
        "pow i:number e:exp=2",
    ]

Are all valid option strings.
