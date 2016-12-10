
from malt.objects import Response as Res, Signature as Sig, Argument as Arg


def test_arg_eq():
    assert Arg(0, "key", "value", None) == Arg(0, "key", "value", None)
    assert Arg(0, "key", "value", None) != Arg(1, "other", "thing", None)


def test_sig_eq():
    one = Sig("cmd", [
        Arg(0, "key", "value", None),
        Arg(1, "other", "thing", None),
    ])
    two = Sig("cmd", [
        Arg(0, "key", "value", None),
        Arg(1, "other", "thing", None),
    ])
    three = Sig("woops", [
        Arg(0, "key", "value", None),
        Arg(1, "other", "thing", None),
    ])
    four = Sig("cmd", [
        Arg(0, "yeah", "ok", None),
        Arg(1, "other", "thing", None),
    ])
    assert one == two
    assert not one != two  # test the __ne__ operator
    assert one != three
    assert one != four
