
import malt

def test_read_empty_file():
    filestring = "\n\n\n"
    responselist = malt.read(filestring, options=['whatever'])
    assert responselist == []


def test_parse_list_empty_default_arg():
    assert malt.parse("a", ["a [i]:list=[]"]).list == []
    assert malt.parse("a list=[1 2 3]", ["a [i]:list=[]"]).list == [1, 2, 3]


def test_parse_dict_empty_default_arg():
    assert malt.parse("a", ["a {s-i}:dict={}"]).dict == {}
    assert malt.parse("a dict={two:2}", ["a {s-i}:dict={}"]).dict == {'two': 2}
