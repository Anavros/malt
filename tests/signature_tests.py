
from malt.objects import Signature, Argument
from malt.parser.signaturebuilder import parse

def test_signature():
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
