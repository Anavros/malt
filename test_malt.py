
import malt
import pytest

def test_fill_exception():
    """When fill does not receive an options list it should throw an error."""
    with pytest.raises(ValueError):
        malt.fill(60)
    with pytest.raises(ValueError):
        malt.fill("This is only technically a list!")
    with pytest.raises(ValueError):
        malt.fill(lambda x: x*x)
    with pytest.raises(ValueError):
        malt.fill(str)
    with pytest.raises(ValueError):
        # even empty lists are invalid
        malt.fill([])

def test_response_parameters():
    response = malt.Response(None)
    assert response == None

    new_response = malt.Response('command', [])
    assert new_response == 'command'

    third_response = malt.Response('command', [('arg1', 'banana'), ('arg2', 33)])
    assert third_response == 'command'
    assert third_response.arg1 == 'banana'
    assert third_response.arg2 == 33

def test_prototype():
    options = ['test', 'add n:int m:int', 'register name']
    prototype = malt._construct_prototype(options)
    assert prototype == {
        'test':
            [],
        'add':
            [('n', int), ('m', int)],
        'register':
            # default to str if no types are given
            [('name', str)],
    }
