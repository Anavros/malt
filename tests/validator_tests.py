
from malt.objects import Response
from malt.parser.validator import validate


def test_validator():
    options = [
        'square i:number',
    ]
    good = Response()
    good.raw_head = 'square'
    good.raw_args = ['5']
    good.raw_kwargs = {}
    good.valid = True

    validated = validate(good, options)
    assert validated.body == {'number': 5}
    assert type(validated.number) is int
