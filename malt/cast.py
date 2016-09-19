
from malt.exceptions import WrongType, NotAnOption, UnexpectedProgrammingError


def auto(mod, value, spec=""):
    bot, top, items = parse_type_specifics(spec)

    if mod == 'i':
        if bot is not None:
            bot = int(bot)
        if top is not None:
            top = int(top)
        if items:
            items = list(map(lambda n: int(n), items))
        return i(value, bot, top, items)
    elif mod == 'f':
        if bot is not None:
            bot = float(bot)
        if top is not None:
            top = float(top)
        if items:
            items = list(map(lambda n: float(n), items))
        return i(value, bot, top, items)
    elif mod == 's':
        return s(value, items)
    elif mod == 'l':
        return l(value)
    elif mod == 'd':
        return d(value, bot, top)
    elif not mod:
        return value
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
        raise WrongType(cast='int', value=value)
    else:
        if bot is not None and top is not None:
            #print('trying range')
            if bot <= value <= top:
                return value
            else:
                raise NotAnOption(value=value, cast='int', bot=bot, top=top)
        elif len(items) > 0:
            #print('trying items')
            if value in items:
                return value
            else:
                raise NotAnOption(value=value, cast='int', options=items)
        else:
            #print('not using spec')
            return value


def f(value, bot, top, items):
    try:
        value = float(value)
    except ValueError:
        raise WrongType(cast='float', value=value)
    else:
        if bot is not None and top is not None:
            if bot <= value <= top:
                return value
            else:
                raise NotAnOption(value=value, cast='float', options=items, bot=bot, top=top)
        elif items:
            if value in items:
                return value
            else:
                raise NotAnOption(value=value, cast='float', options=items, bot=bot, top=top)
        return value


def s(value, items):
    if items:
        if value in items:
            return value
        else:
            raise NotAnOption(value=value, cast='str', options=items, bot=bot, top=top)
    else:
        return value


def l(value):
    value = value.strip('[]').split()
    return value


# BUG: crashes on input similar to {4:5:7}
def d(value, key, val):
    items = {}
    if key is not None and val is not None:
        if key in 'dl' or val in 'dl': raise ValueError("Recursion is a bad idea here!")
        for pair in value.strip('{}').split():
            k, v = pair.split(':')  # throws ValueError on bad input
            items[auto(key, k)] = auto(val, v)
    else:
        for pair in value.strip('{}').split():
            k, v = pair.split(':')  # throws ValueError on bad input
            items[k] = v 
    return items
