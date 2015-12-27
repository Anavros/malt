
# malt for python 3
# written by John Dobbs

# Malt is contained in a single file: simply drag and drop into your project.
import malt

# Provide a list of commands for the user to choose from.
options = [
    'menu',         # commands can be simple, with no arguments
    'order drink',  # or more complicated, with one or more string args
    'tip n:int'     # and can even specify types
]

# Typically menus like this are organized into infinite loops, where the user
# enters a command every iteration. If the command is missing arguments, badly
# typed, or just plain wrong, malt will return an empty response, which will
# fall through the if/else tree and be discarded by the next time around.
while True:
    response = malt.fill(options)

    # Responses can be checked against normal strings.
    if response == 'menu':
        # malt.serve() is a wrapper around print() with support for nested
        # indentation and easy-to-read complex object formatting.
        malt.serve("Our menu includes:")
        # Using malt.indent() will increase the level of indentation for every
        # serving within its block. Indentation can be nested multiple times.
        with malt.indent():
            malt.serve("malt.fill()     - Get a valid command.")
            malt.serve("malt.freefill() - Get an unchecked string.")
            malt.serve("malt.serve()    - Show nicely formatted output.")
            malt.serve("malt.confirm()  - Ask a yes or no question.")
            malt.serve("malt.indent()   - Increase the output indentation.")

    elif response == 'order':
        # Responses are a little more interesting that normal strings.
        # They also hold any extra parameters you've requested from the user.
        # 'order drink' -> response == 'order'; response.drink == [user input]
        drink = response.drink
        if drink in ['fill', 'freefill', 'serve', 'confirm', 'indent']:
            malt.serve("One malt.{}() right away.".format(drink))
        else:
            malt.serve("I'm not sure I know how to make that.")

    elif response == 'tip':
        # Because we specified that n is supposed to be an int, a 'tip'
        # response will only ever be returned if n can safely be cast to int.
        # There is no need to type-check or existence-check at all.
        n = response.n
        if n < 0:
            malt.serve("Very funny. Get out of my example.")
            # Of course the simplest way to exit our loop is to break.
            # Malt also offers a built-in 'quit' command, which allows the user
            # to exit immediately from anywhere (by raising SystemExit).
            break
        elif n < 10:
            malt.serve("Thank you for the tip.")
        else:
            malt.serve("Oh mama! You can come back anytime.")
    # The final else clause is not necessary. If anything is wrong with the
    # user input, malt will print an appropriate error message automatically.
    else:
        pass
