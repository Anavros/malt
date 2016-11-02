
"""
Formatting functions for malt.serve() and malt.log().
"""

def choose_style(item):
    tp = type(item)
    if   tp in [str, int, float]:
        return item, 'str'
    elif tp in [list, set, frozenset]:
        return item, 'list'
    elif tp in [dict]:
        return item, 'dict'
    else:
        try:
            return item.__dict__, 'dict'
        except AttributeError: pass
        try:
            return list(item), 'list'
        except TypeError: pass
        return item, 'str'


# TODO: Add unit tests.
def form(item, end='\n', indent=0, compact=False, depth=0):
    # recursion guard
    if depth >= 5: return str(item)
    string = ""
    item, style = choose_style(item)

    if style == 'str':
        string += (' '*indent + str(item) + end)

    elif style == 'list':
        if len(item) < 1:
            string += '[]' + end
        else:
            if not compact: string += ('[\n')
            indent += 4
            for i, subitem in enumerate(item):
                string += (' '*indent + "[{}] ".format(i))
                string += (form(subitem, '', 0, compact, depth+1) + end)
            indent -= 4
            if not compact: string += (']\n')

    elif style == 'dict':
        if not compact: string += ('{\n')
        indent += 4
        for key, subitem in item.items():
            string += (' '*indent + "{}: ".format(key))
            string += (form(subitem, '\n', 0, compact, depth+1) + end)
        indent -= 4
        if not compact: string += ('}\n')

    return string


def flatten_sequence(items):
    for item in items:
        pass
