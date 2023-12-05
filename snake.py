import pygame, sys
from pygame.locals import *
from enum import Enum
import random

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
NOTVERYWHITE = (252, 252, 252)
RED = (255, 50, 50)
YELLOW = (255, 255, 0)
GREEN = (0,128,0)

BLOCK_SIZE = 20
SCREEN_SIZE = 200

SCREEN_WIDTH = SCREEN_SIZE
SCREEN_HEIGHT = SCREEN_SIZE

FONT_NAME = "Arial"
FONT_SIZE = 36
FONT = pygame.font.Font(None, FONT_SIZE)

isGameOver = False

def DrawGrid(screen):
    for x in range(0, SCREEN_WIDTH, BLOCK_SIZE):
        for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, WHITE, rect, 1)
def setRandomPosition(parts):
    randomX = random.randrange(0, SCREEN_WIDTH, BLOCK_SIZE)
    randomY = random.randrange(0, SCREEN_HEIGHT, BLOCK_SIZE)
    positionIsOk = False
    while positionIsOk == False:
        for part in parts:
            if(part.rect.x == randomX and part.rect.y == randomY):
                positionOk = False
                randomX = random.randrange(0, SCREEN_WIDTH, BLOCK_SIZE)
                randomY = random.randrange(0, SCREEN_HEIGHT, BLOCK_SIZE)
                break
        positionIsOk = True
    applePosition = Position(randomX, randomY)
    return applePosition

class Environment(pygame.sprite.Sprite):
    def __init__(self, s):
        super().__init__()
        self.apple = None
        self.generateNewApple(s)
    def draw(self, surface):
        DrawGrid(surface)
    def generateNewApple(self, snake):
        self.apple = None
        self.apple = Apple(snake)

class Apple(pygame.sprite.Sprite):
    def __init__(self, snake):
        super().__init__()
        self.position = setRandomPosition(snake.parts)
        self.rect = pygame.Rect(self.position.X,self.position.Y, BLOCK_SIZE, BLOCK_SIZE)
    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect, 3, 5)

class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.parts = []
        self.speed = BLOCK_SIZE
        self.move_timer = pygame.time.get_ticks()
        self.move_interval = 700
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
        if(len(self.parts) > 4):
            self.move_interval = 600
        if(len(self.parts) > 9):
            self.move_interval = 500
        if(len(self.parts) > 19):
            self.move_interval = 400
        if(len(self.parts) > 29):
            self.move_interval = 300
        if(len(self.parts) > 39):
            self.move_interval = 250
        if(len(self.parts) > 49):
            self.move_interval = 200
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
        if(self.parts[0].rect.x <0 or self.parts[0].rect.x > (SCREEN_WIDTH-BLOCK_SIZE) or self.parts[0].rect.y <0 or self.parts[0].rect.y > (SCREEN_HEIGHT-BLOCK_SIZE)):
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
        self.snakePosition = position
        self.currentDirection = SnakeDirection.UP
        self.lastDirection = SnakeDirection.UP
        if lastSnakePart is not None:
            self.rect = self.makeSnakePartRect(lastSnakePart)
            self.currentDirection = lastSnakePart.currentDirection
            self.lastDirection = lastSnakePart.lastDirection
        else:
            self.rect = pygame.Rect(BLOCK_SIZE * 4, (BLOCK_SIZE * 5) + (BLOCK_SIZE * self.snakePosition), BLOCK_SIZE, BLOCK_SIZE)
        self.rectToDraw = self.rect
    def draw(self, surface):
        pygame.draw.rect(surface, GREEN, self.rectToDraw, 2, 3)
    def makeSnakePartRect(self, lastSnakePart):
        x= lastSnakePart.rect.left
        y= lastSnakePart.rect.top
        if(lastSnakePart.currentDirection == SnakeDirection.UP):
            y += BLOCK_SIZE
        elif(lastSnakePart.currentDirection == SnakeDirection.DOWN):
            y -= BLOCK_SIZE
        elif(lastSnakePart.currentDirection == SnakeDirection.RIGHT):
            x -= BLOCK_SIZE
        elif(lastSnakePart.currentDirection == SnakeDirection.LEFT):
            x += BLOCK_SIZE
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

class Button:
    def __init__(self, x, y, width, height, text, color, highlight_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.highlight_color = highlight_color
        self.text = text
        self.action = action
        self.clicked = False
    def draw(self, screen):
        color = self.highlight_color if self.clicked else self.color
        pygame.draw.rect(screen, color, self.rect)
        text_surface = FONT.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()
                    self.clicked = True
    def reset_click(self):
        self.clicked = False

def retryAction(snake, env):
    global isGameOver
    isGameOver = False
    snake.direction = SnakeDirection.UP
    snake.parts.clear()
    snake.move_interval = 700
    SPHead = SnakePart(1)
    SP1 = SnakePart(2)
    snake.addPart(SPHead)
    snake.addPart(SP1)
    env.generateNewApple(snake)

def game():
    global isGameOver  
    FPS = 30
    running = True
    FramePerSec = pygame.time.Clock()
    pygame.display.set_caption("snake")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50, "Retry", RED, (255, 100, 100), lambda: retryAction(S,E))

    S = Snake()
    E = Environment(S)
    SPHead = SnakePart(1)
    SP1 = SnakePart(2, SPHead)

    S.addPart(SPHead)
    S.addPart(SP1)

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
                    sys.exit()
            button.handle_event(event)

        if(isGameOver != True):
            S.update(screen)
            if(S.checkAppleCollision(E)):
                SPNew = SnakePart(S.getLength()+1, S.parts[-1])
                S.addPart(SPNew)
                E.generateNewApple(S)
            
            screen.fill(BLACK)

            E.draw(screen)
            E.apple.draw(screen)
            S.draw(screen)
            
            if(S.checkBadCollision()):
                isGameOver = True
            pygame.display.update()
            FramePerSec.tick(FPS)
        else:
            screen.fill(WHITE)
            text_surface = FONT.render("Game Over", True, RED)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text_surface, text_rect)
            button.draw(screen)
            pygame.display.flip()

if __name__=="__main__":
    game()

#TODO: fix the apple generation bug that generates apple inside the snak.