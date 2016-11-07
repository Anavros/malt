
from malt.parser.caster import autocast
from malt.exceptions import BadTypePrefix, WrongType
from pytest import raises


def test_strings():
    assert autocast('string', 's') == 'string'
    assert type(autocast('string', 's')) is str


def test_integers():
    assert autocast('15', 'i') == 15
    assert type(autocast('15', 'i')) is int


def test_floats():
    assert autocast('5.0', 'f') == 5.0
    assert type(autocast('5.0', 'f')) is float


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
        assert autocast(s, 'b') == b


def test_lists():
    assert autocast(['1', '0', '1'], '[b]') == [True, False, True]
    assert type(autocast(['0', '1', '1'], '[b]')) is list
    assert all(type(x) is bool for x in autocast(['0', '1', '1', '0'], '[b]'))


def test_dicts():
    d = {'one':'1', 'two':'0', 'three':'1'}
    result = autocast(d, '{s-i}')
    assert type(result) is dict
    assert result == {'one':1, 'two':0, 'three':1}
    assert all(type(k) is str and type(v) is int for k, v in result.items())


def test_bad_typestring():
    with raises(BadTypePrefix):
        autocast('string', 'lol')


def test_uncastable_value():
    with raises(WrongType):
        autocast('string', 'i')

    with raises(WrongType):
        autocast(['1', '2', 'three'], '[i]')
