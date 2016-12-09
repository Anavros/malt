
from malt.parser.syntaxparser import tokenize, build_response


def test_signature():
    tokens = ['pow', '2', 'power=4']
    result = build_response(tokens)
    assert result.head == 'pow'
    assert result.body[0].position == 0
    assert result.body[0].key == None
    assert result.body[0].value == '2'
    assert result.body[0].cast == None
    assert result.body[1].position == 1
    assert result.body[1].key == 'power'
    assert result.body[1].value == '4'
    assert result.body[1].cast == None


def test_tokenizer():
    line = "keyword scalar [a list] { a:1 dict:2 } def=arg"  # what about deflist=[1 2 3]?
    result = [
        'keyword',
        'scalar',
        ['a', 'list'],
        {'a':'1', 'dict':'2'},
        'def=arg',
    ]
    assert tokenize(line) == result


# TODO;
# Tokens might have to become objects not just primitives.
def hide_test_default_value_list():
    line = "keyword deflist=[1 2 3]"
    assert tokenize(line) == [
        'keyword',
        'deflist=???'  # uh oh: it's supposed to be a list but also a string
    ]


def test_empty_structs():
    line = "keyword [] {}"
    assert tokenize(line) == [
        'keyword',
        [],
        {},
    ]


def test_empty_line():
    assert tokenize("") == []
    sig = build_response([])
    assert sig.head == ''
    assert sig.body == []


def test_only_newline():
    assert tokenize("\n") == [None]
    sig = build_response([None])
    assert sig.head == ''
    assert sig.body == []
