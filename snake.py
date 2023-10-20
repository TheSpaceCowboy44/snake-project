import pygame, sys
from pygame.locals import *
from enum import Enum

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
NOTVERYWHITE = (252, 252, 252)
RED = (255, 50, 50)
YELLOW = (255, 255, 0)

BLOCK_SIZE = 10

SCREEN_WIDTH = 100
SCREEN_HEIGHT = 100

def DrawGrid(screen):
    for x in range(0, SCREEN_WIDTH, BLOCK_SIZE):
        for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, WHITE, rect, 1)
        
class Environment(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.apple = Apple()

    def draw(self, surface):
        DrawGrid(surface)

class Apple(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.position = self.setRandomPosition()
        self.rect = pygame.Rect(self.position.X,self.position.Y, BLOCK_SIZE, BLOCK_SIZE)
    def setRandomPosition():
        #randomX = 
        #TODO GET RANDOM X and Y for apple
        position = Position()
    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect, 1, 3)
class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.parts = []
        self.speed = BLOCK_SIZE
        self.move_timer = pygame.time.get_ticks()
        self.move_interval = 1000
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
    def moveTheDamnSnake(self, now):
        if now - self.move_timer > self.move_interval:
            self.moveParts(self.direction)
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

class SnakePart(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__() 
        self.position = position
        self.rect = pygame.Rect(40,40+(BLOCK_SIZE*self.position), BLOCK_SIZE, BLOCK_SIZE)
        self.currentDirection = SnakeDirection.UP
        self.lastDirection = SnakeDirection.UP
    def draw(self, surface):
        pygame.draw.rect(surface, YELLOW, self.rect, 1, 3)

class Position:
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
class SnakeDirection(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

def getSnakeMovingParams(snakeDirection):
    if(snakeDirection == SnakeDirection.UP):
        return (0, -BLOCK_SIZE)
    if(snakeDirection == SnakeDirection.DOWN):
        return (0, BLOCK_SIZE)
    if(snakeDirection == SnakeDirection.RIGHT):
        return (BLOCK_SIZE, 0)
    if(snakeDirection == SnakeDirection.LEFT):
        return (-BLOCK_SIZE, 0)

def main():
    pygame.init()
    FPS = 30
    FramePerSec = pygame.time.Clock()
    pygame.display.set_caption("snake")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    E = Environment()
    S = Snake()
    SP1 = SnakePart(1)
    SP2 = SnakePart(2)
    SP3 = SnakePart(3)
    
    S.addPart(SP1)
    S.addPart(SP2)
    S.addPart(SP3)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        S.update(screen)
        
        screen.fill(BLACK)
        E.draw(screen)
        S.draw(screen)
            
        pygame.display.update()
        FramePerSec.tick(FPS)

if __name__=="__main__":
    main()

