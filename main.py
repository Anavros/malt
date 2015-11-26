
import malt


def main():
    malt.show("Welcome to malt!")
    malt.show("Let's modify a number for no ostensible reason!")
    
    n = 100
    actions = ["add", "subtract", "halve", "double", "quit"]

    while "bananas are yummy":
        action = malt.ask(actions) 
        if action is None:
            malt.show("unknown command")
            continue

        elif action == "malt-built-in":  # could be cleaner
            continue
        
        elif action == "quit":
            break

        elif action == "add":
            n += 1

        elif action == "subract":
            n -= 1

        elif action == "halve":
            n /= 2

        elif action == "double":
            n *= 2

        else:
            pass

        malt.show("n: {}".format(n))
    malt.show("Quitting...")

if __name__ == "__main__":
    main()
