
from malt.objects import Signature, Argument

"""
...
"""


# Take two signatures full of arguments and combine them into one.
def validate(userinput, signature):
    """
    """
    head = signature.head  # what if they don't match?
    body = []

    # Raises ValueError if any user-given keys are unknown.
    # This happens in a separate step because the iteration coming up only
    # goes over signatures: if there is something extra in userinput, it won't
    # come up. Errors should not be silently ignored, therefore: this step.
    check_for_incorrect_keys(userinput, signature)

    for s in signature:
        try:
            u = match(s, userinput)
        except KeyError:
            # No matches. Just use defaults, if present.
            if s.value is not None:
                # Use the default argument if there is a default.
                body.append(s)
            else:
                # Otherwise we have a problem.
                raise ValueError("No given value and no default either.")
        else:
            body.append(combine(s, u))
    return Signature(head, body)


def check_for_incorrect_keys(userinput, signature):
    known_keys = [s.key for s in signature]
    given_keys = [u.key for u in userinput if u.key is not None]
    if not all(key in known_keys for key in given_keys):
        raise ValueError("Unknown key in user input!")


# Probably where we can implement out-of-order kwargs.
def match(s, userinput):
    """
    Find the user argument that matches the next expected one.
    Raises KeyError if no user arguments match.
    """
    # Try to find the key first.
    for u in userinput:
        if u.key == s.key:
            return u
    # If the key isn't explicitely marked, use the position instead.
    for u in userinput:
        if u.position == s.position:
            if u.key is not None:
                # We found a kwarg where there should be a positional.
                # This is also where we would implement kwarg/arg switching.
                raise ValueError("Found kwarg before end of positional args.")
            else:
                return u
    # If nothing matches, raise KeyError and let the caller handle it.
    raise KeyError("No matches found for {}/{}.".format(s.position, s.key))


def combine(sig, usr):
    """
    Take two halves of the same argument and combine them, using information
    from one to fill in the other.
    """
    # Example:
    # UserInput = Argument(0, None, 'value', None)
    # Signature = Argument(0, 'key', None, 's')
    # Output = Argument(0, 'key', 'value', 's')
    position = sig.position  # might cause problems with out-of-order args
    if usr.key is None:
        # This is a positional argument, no key=value pair, just value.
        key = sig.key
    else:
        # This is a keyword argument, contains both a key and a value.
        key = usr.key  # might cause problems with out-of-order args

    # Guarenteed to have a user value because no value means no argument.
    # And no argument means it will be handled upstream.
    value = usr.value
    cast = sig.cast  # user input never provides casts
    return Argument(position, key, value, cast)
