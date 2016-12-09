
"""
Selects the matching signature for a given userinput.
"""

from malt.objects import Signature, Argument
from malt.exceptions import UnknownKeyword, MissingValue, AmbiguousArgs
from malt.exceptions import UnknownCommand, MismatchedArgs


def find(given, expected):
    """
    Given userinput and a dict of option signatures, select the signature that
    matches the userinput.
    """
    try:
        found = expected[given.head]
    except KeyError:
        raise UnknownCommand from None
    else:
        return found


def match_arguments(userinput, signature):
    """
    Combine user input and option signature into one complete arg list.
    """
    head = signature.head  # what if they don't match?
    body = []

    # Raises an error if the user provides unknown keys or too many pos. args.
    # Done in a separate step because loop below only goes over signatures.
    error_if_bad_argc(userinput, signature)

    for s in signature:
        try:
            u = match(s, userinput)
        except MissingValue:
            # No matches. Just use defaults, if present.
            if s.value is not None:
                # Use the default argument if there is a default.
                body.append(s)
            else:
                # Otherwise we have a problem.
                raise MissingValue()
        else:
            body.append(combine(s, u))
    return Signature(head, body)


def error_if_bad_argc(userinput, signature):
    """
    Raise UnknownKeyword if user input contains an unknown key=value key and
    MismatchedArgs if it has too many positional arguments.
    """
    total_argc = len(signature)
    n_positional_args = sum(1 for arg in userinput.body if arg.key is None)
    known_keys = [s.key for s in signature]
    given_keys = [u.key for u in userinput if u.key is not None]
    if not all(key in known_keys for key in given_keys):
        raise UnknownKeyword()
    if n_positional_args > total_argc:
        raise MismatchedArgs()


def match(s, userinput):
    """
    Find the user argument that matches the next expected one.
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
                raise AmbiguousArgs()
            else:
                return u
    # If nothing matches, raise an error and let the caller handle it.
    raise MissingValue()


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
