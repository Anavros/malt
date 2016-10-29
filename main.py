
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
        'list',
        'dict',
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
            malt.serve(["one","two"])
        elif response.head == 'dict':
            malt.serve({1:"one",2:"two"})
        else:
            malt.handle(response)


if __name__ == '__main__':
    main()
