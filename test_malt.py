
import malt
import pytest

def test_match_case():
    low_options = ['add', 'remove', 'lick']
    mix_options = ['Stifle', 'ruMMage', 'stoRE']
    high_options = ['TEST', 'DISPOSE', 'EXTERMINATE']
    assert malt._match('add', low_options)
    assert malt._match('adD', low_options)
    assert malt._match('stifle', mix_options)
    assert malt._match('RUMMAGE', mix_options)
    assert malt._match('dispose', high_options)
    assert malt._match('EXTerminATE', high_options)

def test_match_space():
    low_options = ['add', 'remove', 'lick']
    mix_options = ['Stifle', 'ruMMage', 'stoRE']
    high_options = ['TEST', 'DISPOSE', 'EXTERMINATE']
    assert malt._match('  lick   \n', low_options)
    assert malt._match('\t\tstore ', mix_options)
    assert malt._match('TEST ', high_options)


def test_not_match():
    low_options = ['add', 'remove', 'lick']
    mix_options = ['Stifle', 'ruMMage', 'stoRE']
    high_options = ['TEST', 'DISPOSE', 'EXTERMINATE']
    assert not malt._match('a d d', low_options)
    assert not malt._match('  STIFLE 10 ', mix_options)
    assert not malt._match('EXPEL \n', high_options)

def test_select_exception():
    with pytest.raises(ValueError):
        # select() must be called with a list of options!
        malt.select("this isn't a list right?")

def test_select_parse():
    options = ['add name:str num:int', 'remove name', 'expand dong:float']
    result = malt._ultra_parse(options)
    assert result == {
        'add': {
            'name': 'str',
            'num': 'int'
        },
        'remove': {
            'name': 'str'
        },
        'expand': {
            'dong': 'float'
        }
    }

def test_select_parse_ugly_input():
    # I don't know why anyone would ever put this as an arg, but...
    options = ['aDD name:str num:INT', '  remove  NamE ', ' exPAND\t\t DONG:float ']
    result = malt._ultra_parse(options)
    assert result == {
        'add': {
            'name': 'str',
            'num': 'int'
        },
        'remove': {
            'name': 'str'
        },
        'expand': {
            'dong': 'float'
        }
    }

def test_select_parse_bad_input():
    with pytest.raises(ValueError):
        malt._ultra_parse(['create:name:int'])

    with pytest.raises(ValueError):
        malt._ultra_parse(['insert:name'])
