
from malt.parser.new import tokenize, convert
from malt.parser.new import Stack
from malt.objects import Signature as Sig, Argument as Arg


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


def test_signature_generation():
    sig = convert(["keyword", "posarg", "key=val", "list=[]"])
    exp = Sig("keyword", [
        Arg(0, None, "posarg", None),
        Arg(1, "key", "val", None),
        Arg(2, "list", "[]", None),
    ])
    assert sig == exp