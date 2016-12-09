
"""
Testing ground for new malt features.
"""

import malt


def main():
    options = [
        '/stuff',          # Dummy placeholder.
        '/add i:n1 i:n2',  # Sum n1 + n2.
        '/pow i:n i:e=2',  # Raise n to power e (default e=2).
        '+ i:i',
    ]
    while True:
        response = malt.offer(options)

        if response == '/stuff':
            print("Correct!")

        elif response == '/add':
            print(response.n1 + response.n2)

        elif response == '/pow':
            print(response.n**response.e)

        elif response == '+':
            print("Adding", response.i)

        else:
            print("Raw input:", response._text)


if __name__ == '__main__':
    main()
