
import readline
import blessings
from itertools import zip_longest
term = blessings.Terminal()

SIDEBAR_X_OFFSET = 0.5

header = "HEADER"
footer = "FOOTER"
sidebar = "SIDEBAR\nMULTI_LINE\nOH YEAH"
prompt = "> "
messages = ["help"]

def message(text):
    messages.insert(0, clean(text))


def set_footer(text):
    global footer
    footer = clean(text)


def set_header(text):
    global header
    header = clean(text)


def set_sidebar(text):
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


def render():
    print(term.clear)

    offsets = {
        'head': 2+len(header.split('\n')),
        'foot': 4+len(footer.split('\n')),
        'side': 0,
    }

    if header:
        head_lines = header.split('\n')
        print(term.move_y(1))
        print(term.bold_yellow('#'*term.width))
        for hl in head_lines:
            print(term.bold_yellow(term.move_x(term.width-2)+' :'), end='')
            print(term.bold_yellow(term.move_x(0)+': '), end='')
            print(hl.strip())
        print(term.bold_yellow('#'*term.width))

    if footer:
        foot_lines = footer.split('\n')
        foot_lines.reverse()
        print(term.move_y(term.height-1))
        print(term.bold_yellow('#'*term.width))
        for fl in foot_lines:
            print(term.move_up*3)
            print(term.bold_yellow(term.move_x(term.width-2)+' :'), end='')
            print(term.bold_yellow(term.move_x(0)+': '), end='')
            print(fl)
        print(term.move_up*3)
        print(term.bold_yellow('#'*term.width))
        #print(term.move_up*3)
        #print("Here's a popup!")

    if sidebar:
        x_off = int(term.width*SIDEBAR_X_OFFSET)
        side_lines = sidebar.split('\n')
        fill_lines = range(offsets['head'], term.height-offsets['head']-offsets['foot'])
        print(term.move_y(offsets['head']))
        for text, i in zip_longest(side_lines, fill_lines, fillvalue=""):
            print(term.move_x(x_off), term.bold_yellow(': '), text)

    if messages:
        offset = len(footer.split('\n'))+6
        print(term.move_y(term.height-offset))
        for s in messages:
            print(s+term.move_up*3)

    print(term.move_y(term.height-2))
