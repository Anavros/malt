
from itertools import zip_longest
import os
from . import state, config


def bless(sidebar_offset=0.5):
    import blessings  # raises uncaught ImportError if missing
    global term
    term = blessings.Terminal()
    config.sidebar_offset = sidebar_offset
    state.blessed = True


def revert():
    state.blessed = False
    os.system('clear')


def mprint(content, end=True, to='body'):
    content = str(content)
    endchar = '\n' if end else ''
    if state.new_line:
        content = (' ' * state.tabs * config.tab_width) + content

    if to == 'head':
        state.head = state.head + content + endchar
    elif to == 'side':
        state.side = state.side + content + endchar
    elif to == 'foot':
        state.foot = state.foot + content + endchar
    else:
        state.body = state.body + content + endchar

    if not state.blessed and to == 'body':
        print(content, end=endchar)

    state.new_line = end


# IDEA: Autoclear after `n` commands.
# Store output in a list and when you autoclear, redraw that output.
def minput():
    print('\n'*config.SPACING_LINES, end='')
    if state.show_new_header and state.new_header:
        print(state.new_header)
    if state.blessed:
        render()
        return input(config.PROMPT)
    else:
        return input(config.PROMPT)


def clear(to='body', bottom_aligned_cursor=True):
    if to == 'head':
        state.head = ''
    elif to == 'side':
        state.side = ''
    elif to == 'foot':
        state.foot = ''
    else:
        state.body = ''
    if not state.blessed and to == 'body':
        if bottom_aligned_cursor:
            # Assuming nobody is using a terminal 100+ lines.
            # Could be configurable.
            print('\n'*100)
        else:
            os.system('clear')


def format_multiline_string_into_list(string, line_width):
    new_lines = []
    raw_lines = string.split('\n')
    if len(raw_lines[-1].strip(' \n')) > 0:
        new_lines.append(" {:<{w}} ".format(raw_lines[-1], w=line_width))
    for s in raw_lines[0:-1]:
        s = s.strip(' \n')
        new_lines.append(" {:<{w}} ".format(s, w=line_width))
    return new_lines


def render():
    print(term.clear)

    head_lines = format_multiline_string_into_list(state.head, term.width-4)
    foot_lines = format_multiline_string_into_list(state.foot, term.width-4)
    side_lines = format_multiline_string_into_list(state.side, 0)
    offsets = {
        'head': 2+len(head_lines) if state.head else 0,
        'foot': 4+len(foot_lines) if state.foot else 0,
        'side': 0,
    }

    if state.head:
        print(term.move_y(1))
        print(term.blue(config.HOR_BAR*term.width))
        for hl in head_lines:
            sides()
            print(term.bold_white_on_black(hl))
        print(term.blue(config.HOR_BAR*term.width))

    if state.foot:
        foot_lines.reverse()
        print(term.move_y(term.height-1))
        print(term.blue(config.HOR_BAR*term.width))
        for fl in foot_lines:
            print(term.move_up*3)
            sides()
            print(term.bold_white_on_black(fl))
        print(term.move_up*3)
        print(term.blue(config.HOR_BAR*term.width))
        #print(term.move_up*3)
        #print("Here's a popup!")

    if state.side:
        x_off = int(term.width*config.sidebar_offset)
        fill_lines = range(offsets['head'], term.height-offsets['head']-offsets['foot'])
        print(term.move_y(offsets['head']))
        for text, i in zip_longest(side_lines, fill_lines, fillvalue=""):
            print(term.move_x(x_off), term.blue(config.VER_BAR),
                term.bold_white(text))

    if state.body:
        lines = state.body.split('\n')
        lines.reverse()
        print(term.move_y(term.height-offsets['foot']))
        for line in lines:
            print(term.move_up*3)
            if line:
                print(line)
            else:
                print()

    print(term.move_y(term.height-2))


def sides():
    print(term.blue(term.move_x(term.width-1)+config.VER_BAR), end='')
    print(term.blue(term.move_x(0)+config.VER_BAR), end='')
