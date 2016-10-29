
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
    elif hasattr(tp, '__dict__'):
        return dict(item.__dict__), 'dict'
    elif hasattr(tp, '__iter__'):
        return list(item), 'list'


# TODO: Add recursion guard.
# TODO: Add unit tests.
def form(item, end='\n', indent=0, compact=False):
    string = ""
    item, style = choose_style(item)

    if style == 'str':
        string += (' '*indent + str(item) + end)

    elif style == 'list':
        if not compact: string += ('[\n')
        indent += 4
        for i, subitem in enumerate(item):
            string += (' '*indent + "[{}] ".format(i))
            string += (form(subitem, '', 0, compact) + end)
        indent -= 4
        if not compact: string += (']\n')

    elif style == 'dict':
        if not compact: string += ('{\n')
        indent += 4
        for key, subitem in item.items():
            string += (' '*indent + "{}: ".format(key))
            string += (form(subitem, '', 0, compact) + end)
        indent -= 4
        if not compact: string += ('}\n')

    return string
