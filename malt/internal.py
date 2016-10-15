
from itertools import zip_longest
import os

tabs = 0
tab_width = 4
max_width = 80
new_line = True
side_offset = 0.5
blessed = False

visible_logs = ['LOG']

head = ""
foot = ""
side = ""
messages = []
body = ""

PROMPT = '> '
PREFIX = '[malt] '
HOR_BAR = '█'
VER_BAR = '▒'


def bless(sidebar_offset=0.5):
    import blessings  # raises uncaught ImportError
    global term, blessed, side_offset
    term = blessings.Terminal()
    side_offset = sidebar_offset
    blessed = True


def revert():
    global blessed
    blessed = False
    os.system('clear')


def show(level):
    global visible_logs
    if level not in visible_logs:
        visible_logs.append(level)


def silence(level):
    global visible_logs
    if level in visible_logs:
        visible_logs.remove(level)


def increase_indentation():
    global tabs
    tabs += 1


def decrease_indentation():
    global tabs
    tabs -= 1


def mprint(content, end=True, to='body'):
    global new_line, body, head, side, foot
    content = str(content)
    endchar = '\n' if end else ''
    if new_line: content = ' '*tabs*tab_width + content

    if to == 'head':
        head = head + content + endchar
    elif to == 'side':
        side = side + content + endchar
    elif to == 'foot':
        foot = foot + content + endchar
    else:
        body = body + content + endchar

    if not blessed and to == 'body':
        print(content, end=endchar)

    new_line = end


def minput():
    if blessed:
        render()
        return input(PROMPT)
    else:
        return input(PROMPT)


def clear(to='body'):
    global body, head, side, foot
    if to == 'head':
        head = ''
    elif to == 'side':
        side = ''
    elif to == 'foot':
        foot = ''
    else:
        body = ''
    if not blessed and to == 'body':
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

    head_lines = format_multiline_string_into_list(head, term.width-4)
    foot_lines = format_multiline_string_into_list(foot, term.width-4)
    side_lines = format_multiline_string_into_list(side, 0)
    offsets = {
        'head': 2+len(head_lines) if head else 0,
        'foot': 4+len(foot_lines) if foot else 0,
        'side': 0,
    }

    if head:
        print(term.move_y(1))
        print(term.blue(HOR_BAR*term.width))
        for hl in head_lines:
            sides()
            print(term.bold_white_on_black(hl))
        print(term.blue(HOR_BAR*term.width))

    if foot:
        foot_lines.reverse()
        print(term.move_y(term.height-1))
        print(term.blue(HOR_BAR*term.width))
        for fl in foot_lines:
            print(term.move_up*3)
            sides()
            print(term.bold_white_on_black(fl))
        print(term.move_up*3)
        print(term.blue(HOR_BAR*term.width))
        #print(term.move_up*3)
        #print("Here's a popup!")

    if side:
        x_off = int(term.width*side_offset)
        fill_lines = range(offsets['head'], term.height-offsets['head']-offsets['foot'])
        print(term.move_y(offsets['head']))
        for text, i in zip_longest(side_lines, fill_lines, fillvalue=""):
            print(term.move_x(x_off), term.blue(VER_BAR),
                term.bold_white(text))

    if body:
        lines = body.split('\n')
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
    print(term.blue(term.move_x(term.width-1)+VER_BAR), end='')
    print(term.blue(term.move_x(0)+VER_BAR), end='')
