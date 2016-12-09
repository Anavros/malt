
import malt

def test_read_empty_file():
    filestring = "\n\n\n"
    responselist = malt.read(filestring, options=['whatever'])
    assert responselist == []


# TODO 
def hide_test_parse_list_empty_default_arg():
    response = malt.parse("a list=[1 2 3]", ["a [i]:list=[]"])
    assert response.list == [1, 2, 3]
