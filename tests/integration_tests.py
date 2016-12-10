
import malt

def test_read_empty_file():
    filestring = [
        "\n",
        "\n",
        "\n",
    ]
    responselist = malt.read(filestring, options=['whatever'])
    assert responselist == []


def test_parse_list_empty_default_arg():
    assert malt.parse("a", ["a [i]:list=[]"]).list == []
    assert malt.parse("a list=[1 2 3]", ["a [i]:list=[]"]).list == [1, 2, 3]


def test_parse_dict_empty_default_arg():
    assert malt.parse("a", ["a {s-i}:dict={}"]).dict == {}
    assert malt.parse("a dict={two:2}", ["a {s-i}:dict={}"]).dict == {'two': 2}


def test_parse_extra_spaces():
    assert malt.parse("a      15", ['a i:n']).n == 15


def test_parse_quoted_string_with_spaces():
    response = malt.parse("a 15 \"slightly chilly\"", ["a i:int string"])
    assert response == 'a'
    assert response.int == 15
    assert response.string == "\"slightly chilly\""  # should strip quotes?


def test_read_with_spaced_strings():
    strings = [
        "a 15 \"slightly chilly\"",
        "a 30 \"warm\"",
    ]
    options = ["a i:int string"]
    lines = malt.read(strings, options)
    assert lines[0].string == '\"slightly chilly\"'
    assert lines[1].string == '\"warm\"'


def test_load_external_file():
    lines = malt.load('tests/testfile.malt', ["a i:temp s:string"])
    assert lines[0].string == "\"cold\""
    assert lines[1].string == "\"pretty chilly\""
    assert lines[2].string == "\"not too bad\""
