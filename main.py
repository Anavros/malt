
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
            print("hi there")
        elif response.head == 'list':
            print(["one","two"], [3, 4])
        elif response.head == 'dict':
            print({1:"one",2:"two"})
        elif response.head == 'test':
            print("line one: ", end='')
            print("still line one: ", end='\n')
            print("line two")
        elif response.head == 'ip':
            print(malt.load('ip.malt'))
        elif response.head == 'response':
            print(response)
        else:
            malt.handle(response)


if __name__ == '__main__':
    with config():
        main()
