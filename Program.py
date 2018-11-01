import pygame
import os
import Actor
import ActorFactory

BACKGROUND_COLOUR = (255, 255, 255)
_image_library = {}
rootFolder = './'
           
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

class NewCatButton:
    '''Button to add a new cat'''

    def __init__(self, image, position, size, actorName, researchTime):
        self.image = getImage(image, size)
        self.position = position
        self.size = size
        self.rect = pygame.Rect(position, size)
        self.actorName = actorName
        self.researchTime= researchTime
        self.researchCounter = self.researchTime

    def click(self, point):
        return self.rect.collidepoint(point)

    def onClicked(self):
        self.researchCounter = 0

    def draw(self, screen):
        screen.blit(self.image, self.position)

        if not self.isAvailable():
            downlight = pygame.Surface(self.size)
            downlight.set_alpha(200)
            downlight.fill((0, 0, 0))
            screen.blit(downlight, self.position)

        researchPercentageComplete = self.researchCounter / self.researchTime
        researchGaugeWidth = self.size[0]*researchPercentageComplete
        researchGaugeHeight = self.size[1]*0.1
        researchGaugeX = self.position[0]
        researchGaugeY = self.position[1] + self.size[1] - researchGaugeHeight
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(researchGaugeX, researchGaugeY, researchGaugeWidth, researchGaugeHeight))

    def update(self):
        if self.researchCounter < self.researchTime:
            self.researchCounter += 1
            
    def isAvailable(self):
        return self.researchCounter >= self.researchTime

        
def log(message):
    print(message)
    
def getImage(path, scale):
    global _image_library
    scaled_image = _image_library.get(path)
    if scaled_image == None:
        full_path = rootFolder + path
        canonicalized_path = full_path.replace('/', os.sep)
        image = pygame.image.load(canonicalized_path)
        scaled_image = pygame.transform.scale(image, (scale[0], scale[1]))
        _image_library[path] = scaled_image
    return scaled_image

def drawBackground(screen):
    screen.fill(BACKGROUND_COLOUR)
    pygame.draw.rect(screen, (10, 150, 10), pygame.Rect(0, screen_height-100, 800, 100))

def drawActors(actors, screen):
    actors.draw(screen)

def updateScreen():
    pygame.display.flip()

def updateGame(actors):
    actors.update()
    for homeSprite in homeSprites:
        if homeSprite.defeated:
            homeSprite.kill()
    for enemySprite in enemySprites:
        if enemySprite.defeated:
            enemySprite.kill()

def addEnemy(actor, xPosition):
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
        newCatButtons.append(NewCatButton(actor.imagePath, (x, screen_height - 50), (40, 40), actor.name, actor.researchTime))
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

addEnemy(actorFactory.create("Basic dog"), screen_width-50)
addEnemy(actorFactory.create("Basic dog"), screen_width)
addEnemy(actorFactory.create("Basic dog"), screen_width+50)

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
    updateGame(actors)
    clock.tick(60)
    updateScreen() 
 
pygame.quit()
    

