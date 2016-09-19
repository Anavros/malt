
import malt

# offer operates basically the same, except with term manip if bless mode
response = malt.offer()

# malt.serve should use the same formatting code, but differ on output style
malt.serve()

# does exactly the same thing
malt.load()

HEADER
FOOTER
SIDEBAR

serve(content, into=HEADER)
