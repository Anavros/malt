
"""
Formatting functions for malt.serve() and malt.log().
"""

def choose_style(tp):
    if   tp in [str, int, float]: return 'str'
    elif tp in [list, set, frozenset]: return 'list'
    elif tp in [dict]: return 'dict'
    else: return 'str'
    #elif tp in []: return ''


def form(item, end='\n', indent=0, compact=False):
    string = ""
    style = choose_style(type(item))

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
