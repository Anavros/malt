
Output Formatting
*****************

`malt.serve()` automatically formats outputs into easy-to-read structures based
on the *types* or *class attributes* of those outputs.

Usage Examples
==============
::

    >>> malt.serve("spam")
    spam
    >>> malt.serve(["ham", "eggs"])
    [
        [0] ham
        [1] eggs
    ]
