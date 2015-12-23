
# malt
a tiny toolkit for making simple interactive text loops

## Purpose
Malt provides a set of tools to help deal with common problems when building
interactive loops on the command prompt.

## Usage

```python
import malt

while True:
    glass = malt.fill(['try', 'buy n:int', 'complain'])

    if glass == 'try':
        with malt.indent():
            malt.serve("Try it, you'll like it!")

    elif glass == 'buy':
        num_copies = response.n
        price_per = 0.0

        malt.serve("That will be ${0}.".format(num_copies*price_per))
        if malt.confirm("Is that ok? "):
            malt.serve("You have purchased {0} copies of this software.".format(num_copies))
        else:
            malt.serve("Come back later; we are having a sale.")

    elif glass == 'complain':
        malt.serve("What exactly are you having trouble with?")
        with malt.indent():
            complaint = malt.freefill()
        malt.serve("I see, you're having trouble with {0}.".format(complaint))
        malt.serve("I'll send that right in and have a look at it soon.")
        del complaint

    elif glass == malt.BACK_CODE:
        if malt.confirm("Are you sure you want to exit? "):
            break
        else:
            continue
```

## Reasoning
TODO: all this nonsense

Malt provides a delectable set of tools that make designing keyword-based 
interactive menus fast and easy.

It's especially well-suited for things like adventure games; where the user 
interacts with the world using keyword commands.

Malt takes the boilerplate out of handling keyword input. You define a list 
of accepted keywords, pass it into malt.select(), and malt will accept user input.

If the user enters one of your keywords, great! You have a cooperative user. 
<code>select()</code> will return the keyword and you can match it however you
please.

On the other hand, if the keyword is misspelled or just plain wrong, <code>select()</code> 
will *not* return the keyword but rather print out a helpful "unknown keyword" 
message and return <code>None</code>. 

By principal, malt will never return impartial or bad input. This relieves you
of the need to error check your input (for correct keywords and type safety of course,
you still need to check the validity of the input with regards to your logic).

Malt is tiny. It all fits into one module, which you can drag and drop into
whatever project needs it. There are a few major functions, couple of extra
features, and a handful of options, so everything is kept as simple as possible
and easy to learn. 

Malt has comprehensive documentation and usage instructions (or it will at least).

In its original prototype, malt was more of a rigid framework than a simple
toolkit. It involved defining and linking all of your functions ahead of time,
submitting them to the library, and calling a run() function which would take
over from there. It wasn't very nice to use. 

The current iteration turned out much better; and it was built with malt's
history in mind. Modern malt leaves the logic and control flow up to you. It
only aims to provide a set of tools, and not interfere with control flow.

Malt is especially good for prototyping simplified versions of more complex
games or applications. Its stripped-down philosophy leads to straightforward
and simple code and fast to develop interfaces.


## Tools
* `fill`: Provide a list of options and in return get the user's choice.
* `freefill`: Get an unprocessed string from the user.
* `serve`: Display a message (print with extra functionality).
* `confirm`: Ask a yes or no question and receive a boolean.
* `indent`: Increase the indentation of the output (used as a contextmanager).
* `savor`: Pause for a moment and let everyone process their thoughts.
* `rinse`: Clear the screen and start anew with a fresh prompt.

### Features
* Input Verification
* Built-in Common Functions
* Flow Control

### options
See [DETAILS](DETAILS.md) for information on specific features.


## Installation
Malt keeps it simple. Drag and drop `malt.py` into your project directory and
`import malt`.

In the future there will likely be a more formal build system; notably to
release onto the PyPi. However malt is purposefully a single file so that it is
easy to install either way.


## Miscellaneous
Malt was written by John Dobbs and is released under the MIT license.

Send me an email if you have any ideas for improvements, and feel free to fork
the repository and send a pull request.
