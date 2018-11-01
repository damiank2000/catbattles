import Actor

class ActorFactory(object):
    '''Factory class to create Actors for the game'''

    def __init__(self, homeSprites, enemySprites):
        self.homeSprites = homeSprites
        self.enemySprites = enemySprites
        self.allActors = {}
        self.allActors["Sweetie"] = self.basicCat
        self.allActors["Tubbs"] = self.bigCat
        self.allActors["Basic dog"] = self.basicDog
        self.allActors["Speedy Catzales"] = self.speedyCat

    def create(self, name):
        return self.allActors[name]()

    def getButtonImage(self, name):
        actor = self.create(name)
        return actor.imagePath

    def basicCat(self):
        return Actor.Actor(name="Sweetie",
                     imagePath="cat1.jpg",
                     width=50,
                     height=50,
                     xVelocity=2,
                     yVelocity=0,
                     attackPower=10,
                     attackFrequency=20,
                     initialEnergy=50,
                     researchTime = 100,
                     enemies=self.enemySprites)

    def bigCat(self):
        return Actor.Actor(name="Tubbs",
                     imagePath="cat2.jpg",
                     width=75,
                     height=75,
                     xVelocity=1,
                     yVelocity=0,
                     attackPower=2,
                     attackFrequency=50,
                     initialEnergy=200,
                     researchTime = 200,
                     enemies=self.enemySprites)

    def speedyCat(self):
        return Actor.Actor(name="Speedy Catzales",
                     imagePath="cat3.jpg",
                     width=40,
                     height=40,
                     xVelocity=5,
                     yVelocity=0,
                     attackPower=1,
                     attackFrequency=1,
                     initialEnergy=5,
                     researchTime = 50,
                     enemies=self.enemySprites)

    def basicDog(self):
        return Actor.Actor(name="Basic dog",
                     imagePath="enemy.png",
                     width=50,
                     height=50,
                     xVelocity=-1,
                     yVelocity=0,
                     attackPower=1,
                     attackFrequency=5,
                     initialEnergy=100,
                     researchTime = 0,
                     enemies=self.homeSprites)
