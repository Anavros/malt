
import malt

def main():
    malt.say("Welcome to Malt!")
    
    fruits = ["peaches", "apples", "mangos", "bananas"]
    favorite = "bananas"
    while "bananas are yummy":
        malt.say("If you can guess my favorite fruit, I'll break this loop!")
        malt.prompt()
        try:
            guess = malt.limited_input(fruits)
        except ValueError:
            malt.say("Nope, try again.")
        else:
            malt.say("You got it!)
            

        if guess == "bananas":
            malt.say("You got it!")
            break
        else:
            malt.say("Nope, try again.")

if __name__ == "__main__":
    main()
