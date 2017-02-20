
"""
Testing ground for new malt features.
"""

import malt


# Alternate method using function signatures.
def stuff():
    print("Correct!")


def add(n1: int, n2: int):
    print(n1 + n2)


def pow(n: int, e: int):
    print(n**e)


def plus(i: int):
    print("Adding", i)


def main():
    while True:
        functions = [stuff, add, pow, plus]
        malt.select_and_run(functions)


def main():
    options = [
        '/stuff',          # Dummy placeholder.
        '/add i:n1 i:n2',  # Sum n1 + n2.
        '/pow i:n i:e=2',  # Raise n to power e (default e=2).
        '+ i:i',
    ]
    options = [
        Option('/stuff'),
        Option('/add', [
            Argument('n1', cast=int),
            Argument('n2', cast=int),
        ]),
        Option('/pow', [
            Argument('n', cast=int),
            Argument('e', cast=int, default=2)
        ]),
        Option('+', [
            Argument('i', cast=int)
        ]),
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
