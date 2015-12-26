"""
Micro Malt
a stripped-down simple version of malt
"""
# a simplified version of malt

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
        serve('[malt] unknown keyword')
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

def serve(output, nl=True):
    print(output, '\n' if nl else '')


# not freeform
# not clear
# not pause
# minimal config features
