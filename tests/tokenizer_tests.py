
from malt.parser.tokenizer import tokenize

def test_tokenizer():
    line = "keyword scalar [a list] { a:1 dict:2 } def=arg"
    result = [
        'keyword',
        'scalar',
        ['a', 'list'],
        {'a':'1', 'dict':'2'},
        'def=',
        'arg',
    ]
    assert tokenize(line) == result
