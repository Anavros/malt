
import pytest
from malt.parser.validator import validate, combine
from malt.objects import UserInput, Signature, Argument as Arg


def test_missing_positional_argument():
    """
    sig: add i:x i:y
    usr: add 5
    val: Error, y not given
    """
    uin = Signature('add', [
        Arg(0, None, '5', None),
    ])
    sig = Signature('add', [
        Arg(0, 'x', None, 'i'),
        Arg(1, 'y', None, 'i'),
    ])
    with pytest.raises(ValueError):
        val = validate(uin, sig)


def test_unknown_keyword():
    """
    sig: add i:x i:y
    usr: add 7 lol=5
    val: Error, lol is not a keyword
    """
    uin = Signature('add', [
        Arg(0, None, '7', None),
        Arg(1, 'lol', '5', None),
    ])
    sig = Signature('add', [
        Arg(0, 'x', None, 'i'),
        Arg(1, 'y', None, 'i'),
    ])
    with pytest.raises(ValueError):
        val = validate(uin, sig)


def est_failure_repeat_same_key():
    """
    sig: add i:x i:y
    usr: add 5 x=10
    val: Error, x specified twice, once positionally, once by keyword
    """
    uin = Signature('add', [
        Arg(0, None, '5', None),  # gets positionally mapped to x
        Arg(1, 'x', '10', None),  # also maps to x, this time by key
    ])
    sig = Signature('add', [
        Arg(0, 'x', None, 'i'),
        Arg(1, 'y', None, 'i'),
    ])
    with pytest.raises(KeyError):
        val = validate(uin, sig)
