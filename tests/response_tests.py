
from malt.objects import Signature, Argument
from malt.parser.responsebuilder import build_response

def test_signature():
    userinput = "pow 2 power=4"
    result = build_response(userinput)
    assert result.head == 'pow'
    assert result.body[0].position == 0
    assert result.body[0].key == None
    assert result.body[0].value == '2'
    assert result.body[0].cast == None
    assert result.body[1].position == 1
    assert result.body[1].key == 'power'
    assert result.body[1].value == '4'
    assert result.body[1].cast == None
