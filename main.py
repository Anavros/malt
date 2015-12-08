
import malt


def main():
    options = ["add", "subtract", "halve", "double"]
    while True:
        action = malt.select(options) 
        if action == malt.BACK_CODE:
            malt.show("Are you sure you would like to exit?")
            if malt.confirm():
                return

        elif action == "add":
            pass

        elif action == "subtract":
            pass

        elif action == "halve":
            pass

        elif action == "double":
            pass

if __name__ == "__main__":
    # Malt will throw an exception if the user enters an exit command.
    try:
        main()
    except malt.AbandonShip:
        pass
