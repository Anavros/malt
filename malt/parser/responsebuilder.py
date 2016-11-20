
from malt.objects import Response


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
            key, value = i, token

        body.append((key, value))
        i += 1
    return Response(head, body)
