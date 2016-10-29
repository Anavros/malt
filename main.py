
"""
Testing ground for new malt features.
"""

import malt
from malt import helpers, state, config

"""
Important Functions:
malt.offer(options)
malt.serve(output)
malt.log(conditional_output)
malt.clear()
malt.set_header()
"""


def main():
    malt.set_header("I'm a header!")
    malt.clear()
    options = [
        'hello',
        'nest',
    ]
    while True:
        response = malt.offer(options)
        if response.head == 'hello':
            malt.serve("hi there")
        elif response.head == 'nest':
            with malt.indent():
                nested_loop()
        else:
            helpers.try_extra_functions(response, options)


def nested_loop():
    options = ['out']
    while True:
        response = malt.offer(options)
        if response.head == 'out':
            break
        else: helpers.try_extra_functions(response, options)


if __name__ == '__main__':
    main()
