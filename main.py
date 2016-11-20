
"""
Testing ground for new malt features.
"""

import malt


def main():
    options = [
        'stuff',          # Dummy placeholder.
        'add i:n1 i:n2',  # Sum n1 + n2.
        'pow i:n i:e=2',  # Raise n to power e (default e=2).
    ]
    while True:
        response = malt.offer(options)
        if response.head == 'stuff':
            print("Correct!")
        elif response.head == 'add':
            print(response.n1 + response.n2)
        elif response.head == 'pow':
            print(response.n**response.e)
        else:
            print("Oh no!")


if __name__ == '__main__':
    main()
