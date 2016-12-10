
from malt.parser.typecaster import cast, _int, _float, _bool, _list, _dict


def test_strings():
    assert cast('string', 's') == 'string'


def test_ints():
    assert cast('15', 'i') == 15


def test_ints_shaped_like_floats():
    assert cast('1.0', 'i') == 1


def test_floats():
    assert cast('5.0', 'f') == 5.0


def test_bools():
    """
    Falsy values include '0' and 'false' (of any letter case).
    Note that '0000' will evaluate to True! This might be a bug.
    """
    assertions = {
        '0': False,
        '1': True,
        'False': False,
        'True': True,
        'fAlSe': False,
        'tRuE': True,
    }
    for s, b in assertions.items():
        assert cast(s, 'b') == b


def test_lists():
    assert _list('[a b c]', 's') == ['a', 'b', 'c']
    assert _list('[1 2 3]', 'i') == [1, 2, 3]


def test_dicts():
    assert _dict('{a:1 b:2}', 's', 'i') == {'a':1, 'b':2}
    #assert _dict('{ a : 1 b : 2 }', 's', 'i') == {'a':1, 'b':2}  # not implimented!
