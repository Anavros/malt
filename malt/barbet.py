
import readline
import blessings
term = blessings.Terminal()

PROMPT = '> '
HEADER = 'THIS IS COOL\nOH YEAH'
INFO_PANEL = "HERE IS SOME HELPFUL INFORMATION\nHEALTH: 100, BUTT: STYLISH"

history = []

def render(header, footer):
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

    print(term.move_y(term.height-7))
    for s in history:
        print(s+term.move_up*3)

    print(term.move_y(term.height-2))
