
import malt
import pytest

def test_matches_case():
    low_options = ['add', 'remove', 'lick']
    mix_options = ['Stifle', 'ruMMage', 'stoRE']
    high_options = ['TEST', 'DISPOSE', 'EXTERMINATE']
    assert malt._matches('add', low_options)
    assert malt._matches('adD', low_options)
    assert malt._matches('stifle', mix_options)
    assert malt._matches('RUMMAGE', mix_options)
    assert malt._matches('dispose', high_options)
    assert malt._matches('EXTerminATE', high_options)

def test_matches_space():
    low_options = ['add', 'remove', 'lick']
    mix_options = ['Stifle', 'ruMMage', 'stoRE']
    high_options = ['TEST', 'DISPOSE', 'EXTERMINATE']
    assert malt._matches('  lick   \n', low_options)
    assert malt._matches('\t\tstore ', mix_options)
    assert malt._matches('TEST ', high_options)


def test_not_matches():
    low_options = ['add', 'remove', 'lick']
    mix_options = ['Stifle', 'ruMMage', 'stoRE']
    high_options = ['TEST', 'DISPOSE', 'EXTERMINATE']
    assert not malt._matches('a d d', low_options)
    assert not malt._matches('  STIFLE 10 ', mix_options)
    assert not malt._matches('EXPEL \n', high_options)
