
from malt.stripper import strip
from malt import joiner

commented_file = r"""
# There are single-line comments...
###
... and multiline comments!
###

# ^ And sometimes empty lines.
command string  # there can even be in-line comments
? command s:arg  # signature hints count as comments too!
    # Some comments will be indented!
  command another_thing  # some legal commands will be indented too!
"""

clean_file = "command string\ncommand another_thing"

to_be_joined = r"""
command [
list
of
arguments
]
command {
1: dict
2: of
3: arguments
}
"""

joined_file = r"""
command [ list of arguments ]
command { 1: dict 2: of 3: arguments }
"""


def test_comment_removal():
    assert strip(commented_file) == clean_file


def test_line_joining():
    assert joiner.collapse_lists(to_be_joined) == joined_file


def test_line_continuation():
    given = (
        "cmd arg1...\n"
        "arg2 arg3\n"
        "cmd arg1"
    )
    result = (
        "cmd arg1 arg2 arg3\n"
        "cmd arg1\n"  # adds an extra newline, benign for now
    )
    assert list(joiner.continue_lines(given)) == list(result)
