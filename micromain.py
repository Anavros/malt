#!/usr/bin/env python3

import micromalt as malt


def main():
    options = [
        'test',
        'list',
        'dict',
    ]
    test_list = "eggs spam sausage bacon ham".split()
    test_dict = {x:i for i,x in enumerate(test_list)}
    while 1:
        response = malt.fill(options)
        if response == 'test':
            malt.serve("it works!")
        elif response == 'list':
            malt.serve(test_list)
        elif response == 'dict':
            malt.serve(test_dict)


if __name__ == '__main__':
    main()
