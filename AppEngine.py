# Created by: Rohan Bansal

import pygame, sys, os
from pygame.locals import *

pygame.init()

sprites = []
texts = []

black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
red = (255, 0, 0)
orange = (255, 140, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
indigo = (128, 0, 128)
violet = (238, 130, 238)

gameDisplay = ""

clock = pygame.time.Clock()

def set_window(title, xInput, yInput):
    global gameDisplay

    gameDisplay = pygame.display.set_mode((xInput, yInput))
    pygame.display.set_caption(title)
    pygame.display.flip()

def disp_width():
    return pygame.display.get_surface().get_size()[0]

def disp_height():
    return pygame.display.get_surface().get_size()[1]

class keyboard():
    def __init__(self):
        self.activeKeys = pygame.key.get_pressed()
    
    def singlePress(self, key):
        foundKeyPressed = False
        for iterEvent in pygame.event.get():
            if iterEvent.type == pygame.KEYDOWN and iterEvent.key == key:
                foundKeyPressed = True
        return foundKeyPressed

class mouse():
    def __init__(self):
        self.update()

    def update(self):
        self.x = pygame.mouse.get_pos()[0]
        self.y = pygame.mouse.get_pos()[1]
    
    def hoverSprite(self, sprite):
        mouseX = pygame.mouse.get_pos()[0]
        mouseY = pygame.mouse.get_pos()[1]
        if sprite.edgeLeft < mouseX < sprite.edgeRight:
            if sprite.edgeTop < mouseY < sprite.edgeBottom:
                return True
        return False
    
    def mouseClicked(self):
        for iterEvent in pygame.event.get():
            if iterEvent.type == pygame.MOUSEBUTTONDOWN:
                return True
        return False

    def spriteClicked(self, sprite):
         if self.hoverSprite(sprite):
            for iterEvent in pygame.event.get():
                if iterEvent.type == pygame.MOUSEBUTTONDOWN:
                    return True
            return False

class text():
    def __init__(self, string, sizeInput, colorInput, xInput, yInput):

        self.textFont = pygame.font.Font("freesansbold.ttf", sizeInput)
        self.textSurface = self.textFont.render(string, True, colorInput)

        self.textString = string
        self.size = sizeInput
        self.color = colorInput
        self.x = xInput
        self.y = yInput
        self.visible = True
        texts.append(self)

    def hide(self):
        self.visible = False
    
    def show(self):
        self.visible = True

    def update(self):
        if self.visible == True:
            gameDisplay.blit(self.textSurface, (self.x, self.y))

    def changeText(self, stringInput, colorInput):
        self.textSurface = self.textFont.render(stringInput, True, colorInput)

    def destroy(self):
        texts.remove(self)
        del(self)

class sprite():
    def __init__(self, image, xInput, yInput, **background):
        if "background" in background:
            self.backG = True
        else:
            self.backG = False
        self.x = xInput
        self.y = yInput
        self.visible = True 
        self.main = pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + "/" + image)
        self.width = self.main.get_rect().size[0]
        self.height = self.main.get_rect().size[1]

        self.rect = self.main.get_rect()

        self.edgeLeft = self.x
        self.edgeRight = self.x + self.width
        self.edgeTop = self.y
        self.edgeBottom = self.y + self.height

        sprites.append(self)

    def hide(self):
        self.visible = False

    def show(self):
        self.visible = True

    def update(self):
        self.edgeLeft = self.x
        self.edgeRight = self.x + self.width
        self.edgeTop = self.y
        self.edgeBottom = self.y + self.height

        if self.visible == True:
            if self.backG == False:
                gameDisplay.blit(self.main, (self.x,self.y))

    def collide(self, otherSprite):
        if otherSprite == None:
            return False
        
        if otherSprite.edgeLeft <= self.edgeLeft <= otherSprite.edgeRight or otherSprite.edgeLeft <= self.edgeRight <= otherSprite.edgeRight:
            if otherSprite.edgeTop <= self.edgeTop <= otherSprite.edgeBottom or otherSprite.edgeTop <= self.edgeBottom <= otherSprite.edgeBottom:
                return True
            else:
                return False

    def destroy(self):
        sprites.remove(self)
        del(self)

    def moveUp(self, speed):
        self.y -= speed
    
    def moveDown(self, speed):
        self.y += speed

    def moveRight(self, speed):
        self.x += speed

    def moveLeft(self, speed):
        self.x -= speed

kb = keyboard()
ms = mouse()

def quitClicked():
    for iterEvent in pygame.event.get():
        if iterEvent.type == pygame.QUIT:
            quit()
            exit()

def gameLoop(background):
    if(isinstance(background, tuple)):
        gameDisplay.fill(background)
    else:
        gameDisplay.blit(background.main, (0, 0))

    quitClicked()

    for sprite in sprites:
        sprite.update()

    for text in texts:
        text.update()

    kb.activeKeys = pygame.key.get_pressed()
    ms.update()

    pygame.display.update()
    clock.tick(60)



