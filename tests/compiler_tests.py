
from malt.compiler import build


def test_compiler():
    tokens = [
        'keyword',
        'scalar',
        ['a', 'list'],
        {'a':'1', 'dict':'2'},
        'def=',
        'arg',
    ]
    response = build(tokens)
    assert response.raw_head == 'keyword'
    assert response.raw_args == ['scalar', ['a', 'list'], {'a':'1', 'dict':'2'}]
    assert response.raw_kwargs == {'def': 'arg'}
