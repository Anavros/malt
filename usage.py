
import malt

options = ['read', 'feed food', 'bleed oz:int']

while True:
    response = malt.select(options)

    elif response == 'read':
        pass

    elif response == 'feed':
        food = response.food

    elif response == 'bleed':
        ounces = response.oz

    elif response == malt.BACK_CODE:
        break
