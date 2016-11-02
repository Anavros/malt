
"""
Testing ground for new malt features.
"""

import malt
import malt.config
from contextlib import contextmanager

"""
Important Functions:
malt.offer(options)
malt.serve(output)
malt.log(conditional_output)
malt.clear()
malt.set_header()
"""


@contextmanager
def config():
    #logfile = open('logfile.txt', 'w')
    #malt.redirect('LOG', logfile)
    yield
    #logfile.close()


def main():
    autocommands = {
        'auto': (lambda: malt.serve('hi there')),
    }
    malt.autocommand(autocommands)
    options = [
        'hello',
        'list',
        'dict',
        'test',
        'ip',
        'response',
    ]
    malt.clear()
    i = 0
    while True:
        i += 1
        malt.set_header("+++ {} +++".format(i))

        response = malt.offer(options)
        if response.head == 'hello':
            malt.log("hi there")
        elif response.head == 'list':
            malt.log(["one","two"], [3, 4])
        elif response.head == 'dict':
            malt.log({1:"one",2:"two"})
        elif response.head == 'test':
            malt.log("line one: ", end='')
            malt.log("still line one: ", end='\n')
            malt.log("line two")
        elif response.head == 'ip':
            malt.serve(malt.load('ip.malt'))
        elif response.head == 'response':
            malt.out(response)
        else:
            malt.handle(response)


if __name__ == '__main__':
    with config():
        main()
