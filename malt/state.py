
"""
Internal state, not to be seen.
"""

tabs = 0
tab_width = 4
max_width = 80
new_line = True

side_offset = 0.5
blessed = False

log_level_blacklist = set()

head = ""
foot = ""
side = ""
messages = []
body = ""

PROMPT = '> '
PREFIX = '[malt] '
HOR_BAR = '█'
VER_BAR = '▒'

command_leader = None
