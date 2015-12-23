
# malt for python 3
# written by John Dobbs

# TODO: short and catchy! Catchy!
# The fastest way to include malt in your project is to drop the malt.py file into your project directory.
# The entire library is contained in one (relatively) short module ready to use.
# You also have the option to install it normally using the setup.py script.

import malt

options = [
    'try',
    'buy copies:int',
    'complain',
]

# Menus are usually orgainized into loops.
# The user can take as much time as they need to enter good commands: all input
# will be validated and vetted by malt. Putting your menu code in a loop allows
# the user to make mistakes.
while True:
    # The big hitter that malt provides is the select() function.
    # It ensures that user input will only be returned if it perfectly matches.
    # If the user tries to enter a bad keyword, too few or too many options, or
    # badly typed options, select() will return None, which will skip over the
    # conditional tree and go right back up to the top.
    # This way you will never get bad, partially-completed input.
    # You don't even need to worry about type checking.
    response = malt.fill(user_options)

    # Once you have your response, you can check it against each option from
    # the original list. The response behaves like a string in equality checks,
    # but also stores any additional parameters that you have asked for.
    if response == 'try':
        malt.show("Try it, you'll like it!")

    elif response == 'buy':
        # 'response' behaves like a string in equality checks, but it is 
        # actually a complex data type. It stores any additional parameters
        # that you've asked for, which are accessible by dot notation.
        num_copies = response.copies
        price_per = 0.0

        malt.show("That will be ${0}.".format(num_copies*price_per))
        if malt.confirm("Is that ok? "):
            malt.show("You have purchased {0} copies of this software.".format(num_copies))
        else:
            malt.show("Come back later; we are having a sale.")

        # There is no need to error check; when you pass in a string parameter,
        # like "buy copies:int", you are guaranteed that 'response' will have
        # a parameter named 'copies' and that 'copies' will be an int.

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

    # The final 'else:' clause is unnecessary and can safely be omitted.
    # If the user enteres a keyword that is not included in the original user_options
    # list, malt will automatcially print out a '[malt] unknown keyword' message.
    else:
        pass

# All of this works together to make it very fast and easy to develop interactive
# keyword menus. What you decide to make is up to you: I personally use malt to
# prototype game ideas quickly. Malt was born from writing the same error-checking
# interface code over and over and over again in different projects.

# Malt also has a few settings and options that can be tweaked as module-level variables... TODO
