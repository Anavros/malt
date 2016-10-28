
"""
Testing ground for new malt features.
"""

import malt
import malt.helpers as helpers


def main():
    options = [
        'hello'
    ]
    while True:
        response = malt.offer(options)
        helpers.try_extra_functions(response, options)


if __name__ == '__main__':
    main()
