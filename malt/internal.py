
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
VER_BAR = '┇'


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


def listify(string, w=0):
    return [" {:<{w}} ".format(s.strip(' \n'), w=w) for s in string.split('\n')]


def render():
    print(term.clear)

    head_lines = listify(head, w=term.width-4)
    foot_lines = listify(foot, w=term.width-4)
    side_lines = listify(side)
    offsets = {
        'head': 2+len(head_lines),
        'foot': 4+len(foot_lines),
        'side': 0,
    }

    if head:
        print(term.move_y(1))
        print(term.bold_yellow(HOR_BAR*term.width))
        for hl in head_lines:
            sides()
            print(term.bold_white_on_black(hl))
        print(term.bold_yellow(HOR_BAR*term.width))

    if foot:
        foot_lines.reverse()
        print(term.move_y(term.height-1))
        print(term.bold_yellow(HOR_BAR*term.width))
        for fl in foot_lines:
            print(term.move_up*3)
            sides()
            print(term.bold_white_on_black(fl))
        print(term.move_up*3)
        print(term.bold_yellow(HOR_BAR*term.width))
        #print(term.move_up*3)
        #print("Here's a popup!")

    if side:
        x_off = int(term.width*side_offset)
        fill_lines = range(offsets['head'], term.height-offsets['head']-offsets['foot'])
        print(term.move_y(offsets['head']))
        for text, i in zip_longest(side_lines, fill_lines, fillvalue=""):
            print(term.move_x(x_off), term.bold_yellow(VER_BAR),
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
    print(term.bold_yellow(term.move_x(term.width-1)+VER_BAR), end='')
    print(term.bold_yellow(term.move_x(0)+VER_BAR), end='')
