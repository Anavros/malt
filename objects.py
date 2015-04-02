
# [GAME] -> Objects
#
# Define your gameplay objects here!
# I find that defining a game through its objects and interactions is very
# helpful. It's much easier for me to focus on the design when I don't worry
# about the implementation.

# Exceptions
class MaltLogicMishap(Exception): pass

# Actors
class Minister(object):
    def __init__(self, name, walk):
        self.name = name
        self.down = False
        self.walk = walk

    def trip(self):
        if not self.down:
            self.down = True
        else:
            raise MaltLogicMishap('%s has already fallen!' % self.name)


# Containers
class SillyWalk(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description
