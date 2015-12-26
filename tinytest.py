#!/usr/bin/env python3

import micromalt as malt


def main():
    options = [
        'test'
    ]
    while 1:
        response = malt.fill(options)
        if response == 'test':
            malt.serve("it works!")


if __name__ == '__main__':
    main()
