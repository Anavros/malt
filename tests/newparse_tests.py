
def test_success():
    assert True


def hide_test_preprocessor():
    from malt.preprocessor import preprocess
    pass


def hide_test_tokenizer():
    from malt.tokenizer import tokenize
    tokens = tokenize("keyword scalar [a list] { a:1 dict:2 } def=arg")
    assert tokens == [
        'keyword',
        'scalar',
        ['a', 'list'],
        {'a':'1', 'dict':'2'},
        'def=',
        'arg',
    ]


def hide_test_compiler():
    from malt.compiler import comp
    response = comp(['command', 'positional', 'keyword', '=', 'default'])
    assert response.raw_head == 'command'
    assert response.raw_args == ['positional']
    assert response.raw_kwargs == {'keyword': 'default'}
