
import malt

def test_success():
    assert True


def test_limited_input():
    mock_inFn = lambda: "my input!"
    mock_options = ["my input!", "wait, that's not right"]
    empty_options = []
    scalar_options = 888
    uppercase_options = ["MY INPUT!", "WAIT, THAT'S NOT RIGHT"]

    assert malt.limited_input(mock_options, inFn=mock_inFn) == "my input!"
    assert malt.limited_input(empty_options, inFn=mock_inFn) == None
    assert malt.limited_input(scalar_options, inFn=mock_inFn) == None
    assert malt.limited_input(uppercase_options, inFn=mock_inFn) == "my input!"


def test_confirm():
    pass


def test_say():
    pass
