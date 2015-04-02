
# [GAME] -> Game
#
# Define how your game objects interact with eachother here!

import objects

# Variables
walk = objects.SillyWalk('Lunge', 'a loose, vaccuuming stride')
minister = objects.Minister('Monty', walk)


# Functions
def push(minister):
    minister.trip()
