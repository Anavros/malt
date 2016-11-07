
"""
Testing ground for new malt features.
"""

import malt


def main():
    options = [
        'stuff',
        'add i:n1 i:n2',
    ]
    while True:
        response = malt.offer(options)
        print(response.body)
        print("Valid:", response.valid)
        if response.head == 'stuff':
            print("Correct!")
        elif response.head == 'add':
            print(response.n1 + response.n2)
        else:
            print("Oh no!")


if __name__ == '__main__':
    main()
