"""
Micro Malt
a stripped-down simple version of malt
"""
def fill(options):
    if not options or type(options) is not list:
        raise ValueError("malt.fill() requires a list of string options.")
    raw = freefill('> ').lower()
    if raw in [o.strip().lower() for o in options]:
        return raw
    elif raw == 'help':
        serve('[malt] Available Commands:')
        serve(options)
    elif raw == 'quit':
        raise SystemExit
    else:
        serve('[malt] Unknown Keyword')
        return None


def freefill(prompt):
    return input(prompt).strip()


def confirm(prompt="[malt] confirm? "):
    while 1:
        raw = freefill(prompt).lower()
        if raw == 'yes':
            return True
        elif raw == 'no':
            return False
        else:
            serve("[malt] (yes/no required)")


def serve(output):
    if type(output) == list:
        for item in output:
            print("* {}".format(item))
    elif type(output) == dict:
        for (k, v) in output.items():
            # should items all print on the same line if not nl?
            print("* {}: ".format(k), end='')
            print(v)
    else:
        print(str(output))
