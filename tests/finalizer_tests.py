
from malt.parser.finalizer import finalize
from malt.objects import Response, Signature, Argument


def test_finalization():
    args = Signature('keyword', [
        Argument(0, 'str', 'value', 's'),
        Argument(1, 'int', '10', 'i'),
        Argument(1, 'float', '1.0', 'f'),
    ])
    response = finalize(args)
    assert response.str == 'value'
    assert response.int == 10
    assert response.float == 1.0
