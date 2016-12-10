
from malt.parser.syntaxparser import tokenize, convert
from malt.parser.syntaxparser import Stack
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


def test_tokenizer_with_excess_spaces():
    # not sure if spaces around ':' or '=' will be allowed
    assert tokenize("keyword    scalar   [a  list] { a:1  dict:2} def=arg deflist=[1 2 3]") == [
        "keyword",
        "scalar",
        "[a  list]",  # unsure if literal spaces will always be preserved like that
        "{ a:1  dict:2}",
        "def=arg",
        "deflist=[1 2 3]",
    ]


def test_quoted_strings():
    assert tokenize("keyword 15 \"this should count as one argument\"") == [
        "keyword",
        "15",
        "\"this should count as one argument\"",
    ]
    assert tokenize("keyword 15 \'this should count as one argument\'") == [
        "keyword",
        "15",
        "\'this should count as one argument\'",
    ]


def test_signature_generation():
    sig = convert(["keyword", "posarg", "key=val", "list=[]"])
    exp = Sig("keyword", [
        Arg(0, None, "posarg", None),
        Arg(1, "key", "val", None),
        Arg(2, "list", "[]", None),
    ])
    assert sig == exp


def test_signature_of_quoted_string():
    sig = convert(['a', 'time', '\"early morning\"'])
    exp = Sig('a', [
        Arg(0, None, 'time', None),
        Arg(1, None, '\"early morning\"', None),
    ])
    assert sig == exp
    assert len(sig) == len(exp)
