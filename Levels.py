class Level(object):
    '''Prototype for a level'''

    def __init__(self):
        self.levelEvents = {}

    def getEvents(self, timer):
        if timer in self.levelEvents:
            return self.levelEvents[timer]
        else:
            return None

class Level1(Level):
    '''Level 1'''

    def __init__(self):
        self.levelEvents = {
            100: "Basic dog",
            200: "Basic dog",
            300: "Basic dog",
            1100: "Basic dog",
            1200: "Basic dog",
            1300: "Basic dog"
            }
