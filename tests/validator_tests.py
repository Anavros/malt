
import pytest
from malt.parser.validator import validate, combine
from malt.objects import UserInput, Signature, Argument as Arg


def test_combination():
    uin = Arg(0, None, '2', None)  # '2'
    sig = Arg(0, 'n', None, 'i')   # 'i:n'
    com = combine(sig, uin)  # order is important!
    assert com.position == 0
    assert com.key == 'n'
    assert com.value == '2'
    assert com.cast == 'i'


def test_easy_validation():
    """
    'pow 8 power=3' + 'pow i:number i:power=2' -> 'pow number=8 power=3'
    """
    uin = Signature('pow', [Arg(0, None, '8', None), Arg(1, 'power', '3', None)])
    sig = Signature('pow', [Arg(0, 'number', None, 'i'), Arg(1, 'power', '2', 'i')])
    val = validate(uin, sig)
    assert val.body[0].position == 0
    assert val.body[0].key == 'number'
    assert val.body[0].value == '8'
    assert val.body[0].cast == 'i'
    assert val.body[1].position == 1
    assert val.body[1].key == 'power'
    assert val.body[1].value == '3'
    assert val.body[1].cast == 'i'


def test_fallback_kwarg():
    """
    'pow 8' + 'pow i:number i:power=2' -> 'pow number=8 power=2'
    """
    uin = Signature('pow', [Arg(0, None, '8', None)])
    sig = Signature('pow', [Arg(0, 'number', None, 'i'), Arg(1, 'power', '2', 'i')])
    # Use default value if kwarg is missing.
    # Positional args can not be missing.
    # Note that argument lists are different lengths.
    val = validate(uin, sig)
    assert val.body[0].position == 0
    assert val.body[0].key == 'number'
    assert val.body[0].value == '8'
    assert val.body[0].cast == 'i'
    assert val.body[1].position == 1
    assert val.body[1].key == 'power'
    assert val.body[1].value == '2'
    assert val.body[1].cast == 'i'


def test_key_inference():
    """
    'pow 8 3' + 'pow i:number i:power=2' -> 'pow number=8 power=3'
    """
    uin = Signature('pow', [Arg(0, None, '8', None), Arg(1, None, '3', None)])
    sig = Signature('pow', [Arg(0, 'number', None, 'i'), Arg(1, 'power', '2', 'i')])
    # Use default value if kwarg is missing.
    # Positional args can not be missing.
    # Note that argument lists are different lengths.
    val = validate(uin, sig)
    assert val.body[0].position == 0
    assert val.body[0].key == 'number'
    assert val.body[0].value == '8'
    assert val.body[0].cast == 'i'
    assert val.body[1].position == 1
    assert val.body[1].key == 'power'
    assert val.body[1].value == '3'
    assert val.body[1].cast == 'i'


def test_key_position_swap():
    """
    'say hi vol=50 tone=mean' + 'say word tone=nice i:vol=100' = 'say hi tone=mean vol=50'
    """
    uin = Signature('say', [
        Arg(0, None, 'hi', None),
        Arg(1, 'vol', '50', None),
        Arg(2, 'tone', 'mean', None),
    ])
    sig = Signature('say', [
        Arg(0, 'word', None, 's'),
        Arg(1, 'tone', 'nice', 's'),
        Arg(2, 'vol', '50', 'i'),
    ])
    # Kwargs can be swapped in position if they both have marked keys when input.
    val = validate(uin, sig)
    assert val.body[0].position == 0
    assert val.body[0].key == 'word'
    assert val.body[0].value == 'hi'
    assert val.body[0].cast == 's'
    assert val.body[1].position == 1
    assert val.body[1].key == 'tone'
    assert val.body[1].value == 'mean'
    assert val.body[1].cast == 's'
    assert val.body[2].position == 2
    assert val.body[2].key == 'vol'
    assert val.body[2].value == '50'
    assert val.body[2].cast == 'i'


def test_explicit_keyword_for_positional_arg():
    """
    sig: add i:x i:y
    usr: add x=5 y=10
    val: add x=5 y=10
    """
    uin = Signature('add', [
        Arg(0, 'x', '5', None),
        Arg(1, 'y', '10', None),
    ])
    sig = Signature('add', [
        Arg(0, 'x', None, 'i'),
        Arg(1, 'y', None, 'i'),
    ])
    val = validate(uin, sig)
    assert val.body[0].position == 0
    assert val.body[0].key == 'x'
    assert val.body[0].value == '5'
    assert val.body[0].cast == 'i'
    assert val.body[1].position == 1
    assert val.body[1].key == 'y'
    assert val.body[1].value == '10'
    assert val.body[1].cast == 'i'
