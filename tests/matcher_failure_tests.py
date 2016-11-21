
import pytest
from malt.parser.matcher import match_arguments, combine
from malt.objects import Signature, Argument as Arg


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
        val = match_arguments(uin, sig)


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
        val = match_arguments(uin, sig)


# Positional arguments are not allowed after the first keyword arg.
def test_positional_arg_after_kwarg():
    """
    sig: pow i:number i:power=2
    usr: pow power=4 8
    val: pow number=8 power=4
    """
    uin = Signature('pow', [
        Arg(0, 'power', '4', None),
        Arg(1, None, '8', None),
    ])
    sig = Signature('pow', [
        Arg(0, 'number', None, 'i'),
        Arg(1, 'power', '2', 'i'),
    ])
    with pytest.raises(ValueError):
        val = match_arguments(uin, sig)
