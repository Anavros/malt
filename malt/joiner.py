

def collapse_lists(filestring):
    joined_string = ""
    in_list = False
    in_dict = False
    for c in filestring:
        if c == '\n':
            if in_list or in_dict:
                joined_string += ' '
            else:
                joined_string += '\n'
        elif c in '[]{}':
            if c == '[':
                if in_list: raise ValueError()
                else: in_list = True
                joined_string += '['
            elif c == ']':
                if not in_list: raise ValueError()
                else: in_list = False
                joined_string += ']'
            elif c == '{':
                if in_dict: raise ValueError()
                else: in_dict = True
                joined_string += '{'
            elif c == '}':
                if not in_dict: raise ValueError()
                else: in_dict = False
                joined_string += '}'
        else:
            joined_string += c
    return joined_string


def continue_lines(filestring):
    joined = ""
    for line in filestring.split('\n'):
        if line[-3:] == '...':
            joined += line[:-3] + ' '
        else:
            joined += line + '\n'
    return joined
