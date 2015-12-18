
# malt
a tiny toolkit for easy console interaction

### usage

```python
import malt

user_options = ['try', 'buy n:int', 'complain']
while True:
    response = malt.select(user_options)

    if response == 'try':
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

### features

### importing into a project

### questions

### contact/contributions/concerns
