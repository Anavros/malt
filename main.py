
# [GAME] -> Main
#
# This is a template starting point for making a game using malt

import sys; sys.dont_write_bytecode = True
import malt
import game
from objects import MaltLogicMishap


def MODE_SILLY():
    def spam():
        malt.out('Replace me with calls to your game logic!')

    def eggs():
        pass

    def trip():
        minister = game.minister
        try:
            game.push(minister)
        except MaltLogicMishap:
            malt.out('But you have already tripped the Minister ' +
                     'of Silly Walks!')
            return
        malt.out('The minister walks with ' + minister.walk.description +
                 ' and it is silly so you trip him.')
        malt.out('You knock over the Minister of Silly Walks.')

    return {"SPAM": spam,
            "EGGS": eggs,
            "PUSH/TRIP": trip}

malt.add_mode('SILLY', MODE_SILLY())

malt.switch_mode('SILLY')
malt.loop()
