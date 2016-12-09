
from malt.parser.new import tokenize


def hide_test_new():
    line = "keyword scalar [a list] { a:1 dict:2 } def=arg deflist=[1 2 3]"
    tokens = tokenize(line)
    assert tokens[0].key == None
    assert tokens[0].val == 'keyword'
    assert tokens[1].val == 'scalar'
    assert tokens[2].val == ['a', 'list']
    assert tokens[3].val == {'a':'1', 'dict':'2'}
    assert tokens[4].key == 'def'
    assert tokens[4].val == 'arg'
    assert tokens[5].key == 'deflist'
    assert tokens[5].val == ['1', '2', '3']
