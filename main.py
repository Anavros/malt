
import malt


def main():
    malt.show("Welcome to malt!")
    malt.show("Let's modify a number for no ostensible reason!")
    malt.show("Ready to start?")

    if not malt.confirm(silent=True):
        return

    malt.SHOW_TITLE_BAR = True
    malt.clear()

    malt.show("What number would you like to start with?")
    n = malt.numeral(1, 100)
    if n is None:
        malt.show("invalid number; using 100 instead")
        n = 100

    malt.show("n: {}".format(n))
    actions = ["add", "subtract", "halve", "double", "quit"]

    while "bananas are yummy":
        action = malt.select(actions) 
        if action is None:
            malt.show("unknown command")
            continue

        elif action == malt.BUILT_IN_CODE:
            continue
        
        elif action == malt.EXIT_CODE:
            if malt.confirm():
                break

        elif action == "add":
            n += 1

        elif action == "subtract":
            n -= 1

        elif action == "halve":
            n /= 2

        elif action == "double":
            n *= 2

        else:
            pass

        malt.show("n: {}".format(n))

if __name__ == "__main__":
    main()
