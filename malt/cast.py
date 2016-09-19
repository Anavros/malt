
from malt.exceptions import WrongType, NotAnOption, UnexpectedProgrammingError


def auto(mod, value, spec=""):
    bot, top, items = parse_type_specifics(spec)

    if mod == 'i':
        return i(value, int(bot), int(top), map(lambda n: int(n), items))
    elif mod == 'f':
        return f(value, float(top), float(bot), map(lambda n: float(n), items))
    elif mod == 's':
        return s(value, spec)
    elif mod == 'l':
        return l(value, spec)
    elif mod == 'd':
        return d(value, spec)
    elif mod == 'o':
        return o(value, spec)
    else: raise UnexpectedProgrammingError()


def parse_type_specifics(spec):
    top = None
    bot = None
    items = []
    if ':' in spec:
        temp = spec.split(':')
        assert len(temp) == 2
        bot, top = tuple(temp)
    elif '|' in spec:
        items = spec.split('|')
    elif spec:
        items = [spec]
    return bot, top, items


# TODO error when top < bot
def i(value, bot, top, items):
    try:
        value = int(value)
    except ValueError:
        raise WrongType()
    else:
        if bot is not None and top is not None:
            print(bot, value, top)
            if bot <= value <= top:
                print('good int')
                return value
            else:
                print('bad int')
                raise NotAnOption()
        elif items:
            if value in items:
                return value
            else:
                raise NotAnOption()
        else:
            return value


def f(value, top, bot, items):
    try:
        value = float(value)
    except ValueError:
        raise WrongType()
    else:
        if top is not None and bot is not None:
            if bot <= value <= top:
                return value
            else:
                raise NotAnOption()
        elif items:
            if value in items:
                return value
            else:
                raise NotAnOption()
        return value


def s(value, spec):
    return value


def l(value, spec):
    return value


def d(value, spec):
    return value


def o(value, spec):
    return value
