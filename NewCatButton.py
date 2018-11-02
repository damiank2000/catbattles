import pygame
import ImageLibrary

class NewCatButton:
    '''Button to add a new cat'''

    def __init__(self, image, position, size, actorName, researchTime):
        self.image = ImageLibrary.getImage(image, size)
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
