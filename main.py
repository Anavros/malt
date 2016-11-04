
"""
Testing ground for new malt features.
"""

import malt


def new_workflow():
    options = [
        'stuff',
    ]
    while True:
        try: response = malt.parse(input('> '), options)
        except (KeyboardInterrupt, EOFError): break
        if response.head == 'stuff':
            print("Correct!")
        else:
            print("Oh no!")


def main():
    options = [
        'hello',
        'list',
        'dict',
        'test',
        'ip',
        'response',
    ]
    while True:
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
    #main()
    new_workflow()
