
"""
Testing ground for new malt features.
"""

import malt
from malt import helpers, enhancements, state, config


def main():
    state.show_new_header = True
    state.new_header = """
        ===UU===
        hell yes
        ===UU===
    """
    config.SPACING_LINES = 2
    malt.clear()
    options = [
        'hello',
        'clear',
    ]
    while True:
        response = malt.offer(options)
        if response.head == 'hello':
            malt.serve("hi there")
        elif response.head == 'clear':
            print("\n"*25)
        else:
            helpers.try_extra_functions(response, options)


if __name__ == '__main__':
    main()
