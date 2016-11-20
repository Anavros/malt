
from malt.parser.tokenizer import tokenize

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
