
from malt.exceptions import WrongType, NotAnOption, UnexpectedProgrammingError


def auto(mod, value, spec=""):
    bot, top, items = parse_type_specifics(spec)

    if mod == 'i':
        return i(value, int(bot) if bot is not None else None,
            int(top) if top is not None else None, map(lambda n: int(n), items))
    elif mod == 'f':
        return i(value, float(bot) if bot is not None else None,
            float(top) if top is not None else None, map(lambda n: float(n), items))
    elif mod == 's':
        return s(value, items)
    elif mod == 'l':
        return l(value)
    elif mod == 'd':
        return d(value, bot, top)
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
        print("bad int cast:", value)
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


def f(value, bot, top, items):
    try:
        value = float(value)
    except ValueError:
        raise WrongType()
    else:
        if bot is not None and top is not None:
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


def s(value, items):
    if items:
        if value in items:
            return value
        else:
            raise NotAnOption()
    else:
        return value


def l(value, bot, top):
    value = value.strip('[]').split()
    return value


# BUG: crashes on input similar to {4:5:7}
def d(value, key, val):
    items = {}
    if key in 'dl' or val in 'dl': raise ValueError("Recursion is a bad idea here!")
    for pair in value.strip('{}').split():
        k, v = pair.split(':')  # throws ValueError on bad input
        items[auto(key, k)] = auto(val, v)
    return items
