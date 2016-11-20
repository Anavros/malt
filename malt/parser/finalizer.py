
from malt.parser.caster import autocast
from malt.objects import Response

"""
The finalizer takes a complete signature and creates a user-usable Response.
"""

def finalize(signature):
    head = signature.head
    body = {}
    for argument in signature.body:
        key = argument.key
        value = autocast(argument.value, argument.cast)
        body[key] = value
    return Response(head, body)
