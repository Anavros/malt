
# malt
a tiny toolkit for making simple interactive text loops

## Purpose
Malt provides a set of tools that help with common problems when building
interactive text loops.

## Usage
See `usage.py`. More examples to come later.

## Reasoning
I like to make a lot of games. Especially simple, text-based ones. It's a
fast way to play around with new ideas or explore a new concept, and it's easy.
But there tends to be a common set of problems that I always run into:
validating user input, dealing with keyword commands, formatting output nicely,
and keeping things easy to develop and tinker with without getting bogged down
as a developer. Malt was born out of a common set of functions that showed up
over and over in every new text game I made. It got some work, a little polish,
and slowly became something worth talking about in its own right.

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
