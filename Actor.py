import pygame

BACKGROUND_COLOUR = (255, 255, 255)

class Actor(pygame.sprite.Sprite):
    '''Main actors for the game'''
        
    def __init__(self,
                 name,
                 imagePath,
                 width,
                 height,
                 xVelocity,
                 yVelocity,
                 attackPower,
                 attackFrequency,
                 initialEnergy,
                 researchTime,
                 enemies):

        super().__init__()

        self.imagePath = imagePath
        self.image = pygame.image.load(imagePath).convert()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.image.set_colorkey(BACKGROUND_COLOUR)
        self.width = width
        self.height = height
        self.rect= self.image.get_rect()
        self.initialXVelocity = xVelocity
        self.initialYVelocity = yVelocity
        self.attackPower = attackPower
        self.energy = initialEnergy
        self.attackFrequency = attackFrequency
        self.attackCount = 0
        self.attackAnimationTime = 5
        self.enemies = enemies
        self.name = name
        self.researchTime = researchTime

        self.attackingSprite = None
        self.defeated = False
        self.striking = False
        self.startMoving()
        
    def setPosition(self, position):
        self.baseY = position[1]
        self.rect.x = position[0]
        self.rect.y = self.baseY
        
    def startMoving(self):
        self.attackingSprite = None
        self.mode = "MOVE"
        self.xVelocity = self.initialXVelocity
        self.yVelocity = self.initialYVelocity
        
    def update(self):
        if self.mode == "ATTACK":
            self.attackCount += 1
            if self.attackCount == self.attackFrequency:
                self.striking = True
            elif self.attackCount == self.attackFrequency + self.attackAnimationTime:
                self.attackingSprite.attacked(self.attackPower, self.name)
                self.attackCount = 0
                self.striking = False
                if self.attackingSprite.defeated:
                    self.startMoving()
        else:
            collidedSprites = pygame.sprite.spritecollide(self, self.enemies, False)
            if len(collidedSprites) > 0:
                self.mode = "ATTACK"
                self.xVelocity = 0
                self.yVelocity = 0
                self.attackingSprite = collidedSprites[0]
            else:
                self.rect.x += self.xVelocity
                self.rect.y += self.yVelocity
        if self.striking == True:
            self.rect.y = self.baseY - 20
        else:
            self.rect.y = self.baseY
        
                
    def attacked(self, attackPower, by):
        self.energy -= attackPower
        if self.energy <= 0:
            self.defeated = True
    
