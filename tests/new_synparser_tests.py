
from malt.parser.new import tokenize
from malt.parser.new import Stack


def test_stack_enclose():
    stack = Stack()
    stack.push('[')
    assert stack.enclosed()
    stack.push(']')
    assert not stack.enclosed()


def test_nested_enclosure():
    stack = Stack()
    stack.push('[')
    assert stack.enclosed()
    stack.push('\"')
    stack.push(']')
    assert stack.enclosed()
    stack.push('\"')


def test_tokenizer_integration():
    assert tokenize("keyword scalar [a list] { a:1 dict:2 } def=arg deflist=[1 2 3]") == [
        "keyword",
        "scalar",
        "[a list]",
        "{ a:1 dict:2 }",
        "def=arg",
        "deflist=[1 2 3]",
    ]
