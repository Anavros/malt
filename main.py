
"""
Testing ground for new malt features.
"""

import malt
import malt.helpers as helpers


def main():
    options = [
    ]
    while True:
        response = malt.offer(options)
        malt.try_globals(response)


if __name__ == '__main__':
    main()
