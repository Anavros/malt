
import readline
import blessings
term = blessings.Terminal()

header = "HEADER"
footer = "FOOTER"
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


def clear():
    global messages
    messages = []


def clean(item):
    if type(item) is not str:
        # maybe it's a list?
        return '\n'.join(map(str, item))
    else:
        return str(item)


def render():
    print(term.clear)

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

    offset = len(footer.split('\n'))+5
    print(term.move_y(term.height-offset))
    for s in messages:
        print(s+term.move_up*3)

    print(term.move_y(term.height-2))
