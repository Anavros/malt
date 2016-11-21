
import pytest
from malt.parser.optionparser import parse, parse_all
from malt.exceptions import EmptyOptionString


def test_signature():
    """
    Parsing takes an option string and creates a Signature. Basic operation test.
    """
    option = "pow i:number i:power=2"
    result = parse(option)
    assert result.head == 'pow'
    assert result.body[0].position == 0
    assert result.body[0].key == 'number'
    assert result.body[0].value == None
    assert result.body[0].cast == 'i'
    assert result.body[1].position == 1
    assert result.body[1].key == 'power'
    assert result.body[1].value == '2'
    assert result.body[1].cast == 'i'


def test_parse_on_no_args():
    """
    Parsing a command with no arguments should not raise any errors.
    """
    result = parse("command")
    assert result.head == "command"
    assert result.body == []


def test_failure_empty_input():
    """
    Raise EmptyOptionString when given empty input.
    """
    with pytest.raises(EmptyOptionString):
        parse('')
