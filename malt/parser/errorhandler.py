
from malt.objects import Response


def mock_response(error):
    try:
        print("[malt]", error.message)
    except AttributeError:
        print("programmer error! unknown error type")
    return Response("", {})
