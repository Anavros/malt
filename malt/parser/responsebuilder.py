
from malt.objects import Signature, Argument


# Does this not throw any errors?
# It's not externally callable, so maybe not?
def build_response(tokens):
    """
    Turn a line of tokens into a Response object.
    """
    head = ""
    body = []
    i = 0
    for token in tokens:
        # The first token always becomes the head.
        if not head:
            head = token
            continue

        # ex: 'key=value'
        if '=' in token:  # TODO: remove hardcode
            key, value = token.split('=', 1)
        else:
            # If a key is not provided, use the integer position of the arg.
            key, value = None, token

        body.append(Argument(i, key, value, None))
        i += 1
    return Signature(head, body)
