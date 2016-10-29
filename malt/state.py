
"""
Internal state, not to be seen by users.
"""

# Used for indentation.
tabs = 0
new_line = True

# If present, a header will be drawn over every prompt.
header = ""

# Any log level in this blacklist will be silenced.
hidden_levels = set()

# History items.
backlog = ""
