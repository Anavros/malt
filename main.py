
"""
Testing ground for new malt features.
"""

import malt

"""
Important Functions:
malt.offer(options)
malt.serve(output)
malt.log(conditional_output)
malt.clear()
malt.set_header()
"""


def main():
    autocommands = {
        'auto': (lambda: malt.serve('hi there')),
    }
    malt.autocommand(autocommands)
    options = [
        'hello',
        'list style=expanded',
    ]
    malt.clear()
    i = 0
    while True:
        i += 1
        malt.set_header("+++ {} +++".format(i))

        response = malt.offer(options)
        if response.head == 'hello':
            malt.serve("hi there")
        elif response.head == 'list':
            malt.serve([1, 2, [4, 5, 5]], compact=(response.style=='compact'))
        else:
            malt.handle(response)


if __name__ == '__main__':
    main()
