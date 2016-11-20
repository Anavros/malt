
from malt.parser.responsebuilder import build_response


def test_compiler():
    tokens = [
        'keyword',
        'scalar',
        ['a', 'list'],
        {'a':'1', 'dict':'2'},
        'def=arg',
    ]
    response = build_response(tokens)
    assert response.head == 'keyword'
    assert response.body == [
        (0, 'scalar'),
        (1, ['a', 'list']),
        (2, {'a':'1', 'dict':'2'}),
        ('def', 'arg'),
    ]
