
import readline
import blessings
from itertools import zip_longest
term = blessings.Terminal()

SIDEBAR_X_OFFSET = 0.5
HOR_BAR = '█'
VER_BAR = '┇'
PROMPT = "> "

header = ""
footer = ""
sidebar = ""
messages = [""]

def slide(text):
    for line in text.split('\n'):
        messages.insert(0, clean(line))
    messages.insert(0, '')


def foot(text):
    global footer
    footer = clean(text)


def head(text):
    global header
    header = clean(text)


def side(text):
    global sidebar
    sidebar = clean(text)


def clear():
    global messages
    messages = []


def clean(item):
    if type(item) is list:
        return '\n'.join(map(str, item))
    else:
        return str(item)


def listify(string, w=0):
    return [" {:<{w}} ".format(s.strip(' \n'), w=w) for s in string.split('\n')]


def render():
    print(term.clear)

    head_lines = listify(header, w=term.width-4)
    foot_lines = listify(footer, w=term.width-4)
    side_lines = listify(sidebar)
    offsets = {
        'head': 2+len(head_lines),
        'foot': 4+len(foot_lines),
        'side': 0,
    }

    if header:
        print(term.move_y(1))
        print(term.bold_yellow(HOR_BAR*term.width))
        for hl in head_lines:
            sides()
            print(term.bold_white_on_black(hl))
        print(term.bold_yellow(HOR_BAR*term.width))

    if footer:
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

    if sidebar:
        x_off = int(term.width*SIDEBAR_X_OFFSET)
        fill_lines = range(offsets['head'], term.height-offsets['head']-offsets['foot'])
        print(term.move_y(offsets['head']))
        for text, i in zip_longest(side_lines, fill_lines, fillvalue=""):
            print(term.move_x(x_off), term.bold_yellow(VER_BAR),
                term.bold_white(text))

    if messages:
        print(term.move_y(term.height-offsets['foot']))
        for s in messages:
            print(term.move_up*3)
            if s:
                print(PROMPT+s.strip())
            else:
                print()

    print(term.move_y(term.height-2))


def sides():
    print(term.bold_yellow(term.move_x(term.width-1)+VER_BAR), end='')
    print(term.bold_yellow(term.move_x(0)+VER_BAR), end='')
