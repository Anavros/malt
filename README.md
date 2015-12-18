
# malt
a tiny toolkit for making simple interactive text loops

## usage

```python
import malt

while 1:
    response = malt.select(['try', 'buy n:int', 'complain'])

    if response == 'try':
        with malt.indent():
            malt.show("Try it, you'll like it!")

    elif response == 'buy':
        num_copies = response.n
        price_per = 0.0

        malt.show("That will be ${0}.".format(num_copies*price_per))
        if malt.confirm("Is that ok? "):
            malt.show("You have purchased {0} copies of this software.".format(num_copies))
        else:
            malt.show("Come back later; we are having a sale.")

    elif response == 'complain':
        malt.show("What exactly are you having trouble with?")
        with malt.indent():
            complaint = malt.freeform()
        malt.show("I see, you're having trouble with {0}.".format(complaint))
        malt.show("I'll send that right in and have a look at it soon.")
        del complaint

    elif response == malt.BACK_CODE:
        if malt.confirm("Are you sure you want to exit? "):
            break
        else:
            continue
```

## Reasoning
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

## Details
select
confirm
indent
show

### options
built-in option handling
keywords
indentation settings
codes

### importing into a project
no official build system yet
just drag and drop

## Questions
will malt buy my groceries for me?

### contact/contributions/concerns
Malt was written by John Dobbs and released under the MIT license.
Send me an email if you have any ideas for improvements, and feel free to fork
the repository and send a pull request.
