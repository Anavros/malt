
# Malt
#
# A simple, text-based game framework

# TODO
# Add proper documentation
# Branch off into a more advanced version using curses
import os  # Temporary for testing...

MODES = {}
ACTIVE = None


def add_mode(name, mode):
    # The first mode that is added will be the one in which the game starts.
    global ACTIVE
    if name not in MODES.keys():
        MODES[name] = mode
        if ACTIVE is None:
            ACTIVE = name
    else:
        raise KeyError('%s is already a known mode!' % name)


def switch_mode(name):
    global ACTIVE
    if name in MODES.keys():
        ACTIVE = name


def get_input(string):
    return raw_input(string).strip().upper()


def command(mode):
    # If multiple functions are linked with the same command,
    # all will be called by that command, in order
    response = get_input('>>> ')

    # Special Cases
    if response in ['QUIT', 'EXIT']:
        import sys
        sys.exit()
    if response in ['HELP', 'LIST', 'LS']:
        print mode.keys()

    # For testing...
    if response == 'MODE':
        print ACTIVE
    if response == 'CLEAR':
        os.system('clear')

    # Normal Conditions
    for string in mode.keys():
        synonyms = string.split('/')
        if response in synonyms:
            mode[string]()


def loop():
    while True:
        command(MODES[ACTIVE])


def prompt(string, options=[]):
    string = string.upper() + ': '
    response = get_input(string)
    if options:
        while response not in options:
            response = get_input(string)
            print response in options
    return response


def confirm(string):
    response = get_input(string + '\n' + 'Y/N: ')
    return response in ['YES', 'Y', 'YEAH', 'YEP', 'PLEASE']

def out(data, format=''):
    if not format:
        print data
    elif format == 'FANCY':
        print '*** %s ***' % data
    elif format == 'TITLE':
        print '        ===%s===' % data
    elif format == 'LIST':
        print data
    else:
        print data
        print 'Malt does not understand the %s format!' % format
