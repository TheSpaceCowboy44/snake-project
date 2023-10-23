import pygame, sys
from pygame.locals import *
from enum import Enum
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
NOTVERYWHITE = (252, 252, 252)
RED = (255, 50, 50)
YELLOW = (255, 255, 0)

BLOCK_SIZE = 20
SCREEN_SIZE = 200

SCREEN_WIDTH = SCREEN_SIZE
SCREEN_HEIGHT = SCREEN_SIZE

def DrawGrid(screen):
    for x in range(0, SCREEN_WIDTH, BLOCK_SIZE):
        for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, WHITE, rect, 1)

def setRandomPosition():
    randomX = random.randrange(0, SCREEN_WIDTH, BLOCK_SIZE)
    randomY = random.randrange(0, SCREEN_HEIGHT, BLOCK_SIZE)
    return Position(randomX, randomY)

class Environment(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.apple = None
        self.generateNewApple()
    def draw(self, surface):
        DrawGrid(surface)
    def generateNewApple(self):
        self.apple = None
        self.apple = Apple()

class Apple(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.position = setRandomPosition()
        self.rect = pygame.Rect(self.position.X,self.position.Y, BLOCK_SIZE, BLOCK_SIZE)
    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect, 3, 5)
class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.parts = []
        self.speed = BLOCK_SIZE
        self.move_timer = pygame.time.get_ticks()
        self.move_interval = 750
        self.direction = SnakeDirection.UP

    def update(self, surface):
        pressed_keys = pygame.key.get_pressed()
        hasMoved = False
        now = pygame.time.get_ticks()
        
        if pressed_keys[K_UP] and hasMoved == False:
            self.direction = SnakeDirection.UP
            hasMoved = True
    
        if pressed_keys[K_DOWN] and hasMoved == False:
            self.direction = SnakeDirection.DOWN
            hasMoved = True
    
        if pressed_keys[K_LEFT] and hasMoved == False:
            self.direction = SnakeDirection.LEFT
            hasMoved = True
    
        if pressed_keys[K_RIGHT] and hasMoved == False:
            self.direction = SnakeDirection.RIGHT
            hasMoved = True

        self.moveTheDamnSnake(now)

    def draw(self, surface):
        for part in self.parts:
            part.draw(surface)
    def addPart(self, snakePart):
        self.parts.append(snakePart)
    def removePart(self):
        self.parts.pop()
    def getLength(self):
        return len(self.parts)
    def checkSnakeDirection(self):
        snakeLastDirection = self.parts[0].currentDirection
        if(self.direction == SnakeDirection.UP and snakeLastDirection != SnakeDirection.DOWN):
            return True
        if(self.direction == SnakeDirection.DOWN and snakeLastDirection != SnakeDirection.UP):
            return True
        if(self.direction == SnakeDirection.RIGHT and snakeLastDirection != SnakeDirection.LEFT):
            return True
        if(self.direction == SnakeDirection.LEFT and snakeLastDirection != SnakeDirection.RIGHT):
            return True
        return False
    def moveTheDamnSnake(self, now):
        if now - self.move_timer > self.move_interval:
            if(self.checkSnakeDirection()):
                self.moveParts(self.direction)
            else:
                self.moveParts(self.parts[0].currentDirection)
            self.move_timer = now
    def moveParts(self, newDirection):
        self.parts[0].lastDirection = self.parts[0].currentDirection
        self.parts[0].currentDirection = newDirection
        x, y = getSnakeMovingParams(self.parts[0].currentDirection)
        self.parts[0].rect.move_ip(x,y)
        for idPart in range(1, len(self.parts)):
            part = self.parts[idPart]
            part.lastDirection = part.currentDirection
            part.currentDirection = self.parts[idPart-1].lastDirection
            x, y = getSnakeMovingParams(part.currentDirection)
            part.rect.move_ip(x, y)
            self.parts[idPart] = part
        return
    def checkBadCollision(self):
        if(self.parts[0].rect.x <0 or self.parts[0].rect.x > SCREEN_WIDTH or self.parts[0].rect.y <0 or self.parts[0].rect.y > SCREEN_HEIGHT):
            return True
        for part in self.parts[1:]:
            if(self.parts[0].rect.x == part.rect.x and self.parts[0].rect.y == part.rect.y):
                return True
        return False
    def checkAppleCollision(self, env):
        if(self.parts[0].rect.x == env.apple.position.X and self.parts[0].rect.y == env.apple.position.Y):
            return True
        return False

class SnakePart(pygame.sprite.Sprite):
    def __init__(self, position, lastSnakePart=None):
        super(SnakePart, self).__init__()  
        self.position = position
        self.currentDirection = SnakeDirection.UP
        self.lastDirection = SnakeDirection.UP

        if lastSnakePart is not None:
            self.rect = self.makeSnakePartRect(lastSnakePart)
            self.currentDirection = lastSnakePart.currentDirection
            self.lastDirection = lastSnakePart.lastDirection
        else:
            self.rect = pygame.Rect(BLOCK_SIZE * 3, (BLOCK_SIZE * 3) + (BLOCK_SIZE * self.position), BLOCK_SIZE, BLOCK_SIZE)

    def draw(self, surface):
        pygame.draw.rect(surface, YELLOW, self.rect, 1, 3)

    def makeSnakePartRect(self, lastSnakePart):
        x= lastSnakePart.rect.left
        y= lastSnakePart.rect.top
        if(lastSnakePart.currentDirection == SnakeDirection.UP):
            y = y+BLOCK_SIZE
        elif(lastSnakePart.currentDirection == SnakeDirection.DOWN):
            y = y-BLOCK_SIZE
        elif(lastSnakePart.currentDirection == SnakeDirection.RIGHT):
            x = x-BLOCK_SIZE
        elif(lastSnakePart.currentDirection == SnakeDirection.LEFT):
            x = x+BLOCK_SIZE
        else:
            print("fail")
        newRect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
        return newRect

class Position:
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
class SnakeDirection(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

def getSnakeMovingParams(snakeCurrentDirection):
    if(snakeCurrentDirection == SnakeDirection.UP):
        return (0, -BLOCK_SIZE)
    if(snakeCurrentDirection == SnakeDirection.DOWN):
        return (0, BLOCK_SIZE)
    if(snakeCurrentDirection == SnakeDirection.RIGHT):
        return (BLOCK_SIZE, 0)
    if(snakeCurrentDirection == SnakeDirection.LEFT):
        return (-BLOCK_SIZE, 0)

def main():
    pygame.init()
    FPS = 30
    FramePerSec = pygame.time.Clock()
    pygame.display.set_caption("snake")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    E = Environment()
    S = Snake()
    SPHead = SnakePart(1)
    SP1 = SnakePart(2)
    
    apple1 = Apple()
    apple2 = Apple()
    apple3 = Apple()

    S.addPart(SPHead)
    S.addPart(SP1)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        S.update(screen)
        if(S.checkAppleCollision(E)):
            SPNew = SnakePart(S.getLength()+1, S.parts[-1])
            S.addPart(SPNew)
            E.generateNewApple()
        
        screen.fill(BLACK)

        E.draw(screen)
        E.apple.draw(screen)
        S.draw(screen)
        
        if(S.checkBadCollision()):
            pygame.quit()
            sys.exit()
        pygame.display.update()
        FramePerSec.tick(FPS)

if __name__=="__main__":
    main()

