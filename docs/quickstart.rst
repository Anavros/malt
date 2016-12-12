
Getting Started
***************

When taking input, you specify which commands the user is allowed to enter::

    response = malt.offer(['apple', 'banana', 'orange'])

In this case, the user is only allowed to enter one of 'apple', 'banana', or
'orange'. In order to make user commands more powerful, you can add arguments::

    options = [
        'apple',
        'banana',
        'orange',
    ]
    response = malt.offer(options)
