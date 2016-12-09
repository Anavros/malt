
import malt

def test_read_empty_file():
    filestring = "\n\n\n"
    responselist = malt.read(filestring, options=['whatever'])
    assert responselist == []
