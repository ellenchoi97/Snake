import pygame
from random import randint

RECT_SIZE = 20
SCREEN_DIMEN = 500
MAX_SCREEN_EDGE = SCREEN_DIMEN - 20

class Square:
    def __init__(self, posX, posY, theColor):
        self.x = posX
        self.y = posY
        self.color = theColor

    def moveSquare(self, newX, newY):
        self.x = newX
        self.y = newY

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, RECT_SIZE, RECT_SIZE))

#The Food class contains the food's x and y values
class Food:
    def __init__(self, theColor):
        self.square = Square(RECT_SIZE * randint(0, MAX_SCREEN_EDGE / RECT_SIZE),
                             RECT_SIZE * randint(0, MAX_SCREEN_EDGE / RECT_SIZE),
                             theColor)

    def getPos(self):
        return (self.square.x, self.square.y)

    def resetPos(self):
        self.square.moveSquare(RECT_SIZE * randint(0, MAX_SCREEN_EDGE / RECT_SIZE),
                               RECT_SIZE * randint(0, MAX_SCREEN_EDGE / RECT_SIZE))

    def draw(self, screen):
        self.square.draw(screen)

#The player class contain's the player's body list
class Player:
    def __init__(self, theColor, posX, posY, theDirection):
        self.body = [Square(posX, posY, theColor)]
        self.startX = posX
        self.startY = posY
        self.color = theColor
        self.direction = theDirection
        self.startDir = theDirection

    def addBody(self):
        self.body.append(Square(0, 0, self.color))

    def moveBody(self):
        #Move all body parts to their next location
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].moveSquare(self.body[i-1].x, self.body[i-1].y)

        #Move the snake's head to the next location    
        if self.direction == "up":
            self.body[0].y -= RECT_SIZE
        elif self.direction == "down":
            self.body[0].y += RECT_SIZE
        elif self.direction == "left":
            self.body[0].x -= RECT_SIZE
        elif self.direction == "right":
            self.body[0].x += RECT_SIZE

    def resetPlayer(self):
        self.body = [Square(self.startX, self.startY, self.color)]
        self.direction = self.startDir

    def checkBoundary(self, left, right, top, bottom):
        #If the snake hits a boundary
        if (self.body[0].x < left or self.body[0].x > right or
            self.body[0].y < top or self.body[0].y > bottom):
            return True
        return False

    def checkSelfDestroy(self):
        #If the snake eats itself
        for i in range(1, len(self.body)):
            if (self.body[0].x == self.body[i].x and
                self.body[0].y == self.body[i].y):
                return True
        return False

    def eatFood(self, foodPos):
        #If the snake eats the food
        if foodPos[0] == self.body[0].x and foodPos[1] == self.body[0].y:
            self.addBody()
            return True
        return False

    def draw(self, screen):
        for i in range(len(self.body)):
            pygame.draw.rect(screen, self.color, (self.body[i].x, self.body[i].y,
                                                  RECT_SIZE, RECT_SIZE))

class Image:
    def __init__(self, filename, posY, scaleX=-1, scaleY=-1):
        self.image = pygame.image.load(filename)
        if scaleX != -1 and scaleY != -1:
            self.image = pygame.transform.scale(self.image, (scaleX, scaleY))
        self.boundingRect = self.image.get_rect()
        
        self.x = (SCREEN_DIMEN - self.boundingRect.width) / 2
        self.y = posY
        self.boundingRect.left = self.x
        self.boundingRect.top = posY
        
    def checkClicked(self, collideX, collideY):
        if self.boundingRect.collidepoint(collideX, collideY):
            return True
        return False

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
