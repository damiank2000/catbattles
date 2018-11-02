import pygame
import ImageLibrary
import Actor
import ActorFactory
import NewCatButton
import Levels

BACKGROUND_COLOUR = (255, 255, 255)
timer = 0

class Base(pygame.sprite.Sprite):
    '''Base sprite'''
    
    def __init__(self, name, colour, x, y, width, height, initialEnergy):

        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(colour)
        self.rect= self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.energy = initialEnergy
        self.name = name
        self.defeated = False

    def attacked(self, attackPower, by):
        log(self.name + ' attacked by ' + by + ' for ' + str(attackPower) + ' damage')
        self.energy -= attackPower
        if self.energy <= 0:
            print(self.name + ' defeated!')
        
def log(message):
    print(message)

def drawBackground(screen):
    screen.fill(BACKGROUND_COLOUR)
    pygame.draw.rect(screen, (10, 150, 10), pygame.Rect(0, screen_height-100, 800, 100))

def drawActors(actors, screen):
    actors.draw(screen)

def updateScreen():
    pygame.display.flip()

def updateGame(actors, level):
    global timer
    timer += 1
    actors.update()
    for homeSprite in homeSprites:
        if homeSprite.defeated:
            homeSprite.kill()
    for enemySprite in enemySprites:
        if enemySprite.defeated:
            enemySprite.kill()
    event = level.getEvents(timer)
    if not event == None:
        addEnemy(actorFactory.create(event))

def addEnemy(actor):
    xPosition = screen_width
    actor.setPosition((xPosition, screen_height-75-actor.height))
    actors.add(actor)
    enemySprites.add(actor)
    actor.startMoving()

def addFriend(actor, xPosition):
    actor.setPosition((xPosition, screen_height-75-actor.height))
    actors.add(actor)
    homeSprites.add(actor)
    actor.startMoving()

def getNewCatButtons(team, actorFactory):
    newCatButtons = []
    x = 10
    for teamMember in team:
        actor = actorFactory.create(teamMember)
        newCatButtons.append(NewCatButton.NewCatButton(actor.imagePath, (x, screen_height - 50), (40, 40), actor.name, actor.researchTime))
        x += 50               
    return newCatButtons


pygame.init() 
screen_width = 800
screen_height = 400
base_height = 100
base_width = 80
screen = pygame.display.set_mode([screen_width, screen_height])
actors = pygame.sprite.Group()
enemySprites = pygame.sprite.Group()
homeSprites = pygame.sprite.Group()
clock = pygame.time.Clock()
actorFactory = ActorFactory.ActorFactory(homeSprites, enemySprites)
team = [
    "Sweetie",
    "Tubbs",
    "Speedy Catzales"
    ]
newCatButtons = getNewCatButtons(team, actorFactory)

homeBase = Base("Home base", (10, 10, 150), 10, screen_height-100-base_height+10, base_width, base_height, 50)
actors.add(homeBase)
homeSprites.add(homeBase)

enemyBase = Base("Enemy base", (150, 10, 10), screen_width-base_width-10, screen_height-100-base_height+10, base_width, base_height, 50)
actors.add(enemyBase)
enemySprites.add(enemyBase)

level = Levels.Level1()

# -------- Main Program Loop -----------
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONUP:
            for button in newCatButtons:
                if button.isAvailable() & button.click(pygame.mouse.get_pos()):
                    addFriend(actorFactory.create(button.actorName), 0)
                    button.onClicked()
 
    drawBackground(screen)
    drawActors(actors, screen)
    for button in newCatButtons:
        button.update()
        button.draw(screen)
    updateGame(actors, level)
    clock.tick(60)
    updateScreen() 
 
pygame.quit()
    

