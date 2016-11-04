
from malt.stripper import strip

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
###
And we don't want none of this shit.
This module gets rid of all these stinkin' comments, and the whitespace too.
###
"""

def test_single_removal():
    pass
