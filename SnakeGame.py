#!/usr/bin/env python3

import pygame
import random
import time

def _computeRect(cx,cy,game):
    x = cx - (game.MAP_WIDTH // game.GRID_X) // 2
    y = cy - (game.MAP_HEIGHT // game.GRID_Y) // 2
    w = game.MAP_WIDTH // game.GRID_X
    h =  game.MAP_HEIGHT // game.GRID_Y
   
    return (x,y,w,h)

class Game(object):
    def __init__(self,width,height,gridX,gridY):
        self.MAP_WIDTH  = width
        self.MAP_HEIGHT = height
        self.GRID_X = gridX
        self.GRID_Y = gridY
        self.randomApple([])        

    def randomApple(self,snakeTrail):
        self.appleX = random.randint(0,self.GRID_X - 1)
        self.appleY = random.randint(0,self.GRID_Y - 1)

        while (self.appleX,self.appleY) in snakeTrail:
            self.appleX = random.randint(0,self.GRID_X - 1)
            self.appleY = random.randint(0,self.GRID_Y - 1)

        self.appleX = (self.appleX + 0.5) * self.MAP_WIDTH // self.GRID_X 
        self.appleY = (self.appleY + 0.5) * self.MAP_HEIGHT // self.GRID_Y

class Snake(object):
    def __init__(self,game,startPos):
        self.game            = game
        self.x, self.y       = startPos[0],startPos[1]
        self._velX, self._velY = 0,0
        self.trail           = []
        self.alive           = True


    def update(self):
        if self.alive:
            prevX, prevY = self.x,self.y
            
            #can only move when the snake snaps on the grid

            self.x = (self.x + self.velX)
            self.y = (self.y + self.velY)
            
            #check if the snake has moved
            if not ((self.x,self.y) == (prevX,prevY)):
                self.trail.append((prevX,prevY))
            
                for x,y in self.trail:
                    if self.x == x and self.y == y:
                        self.alive = False

                x,y = (self.x, self.y)
                if x < 0 or y < 0 or x >= self.game.MAP_WIDTH or y >= self.game.MAP_HEIGHT:
                    self.alive = False

                if x == self.game.appleX and y == self.game.appleY:
                    self.game.randomApple(self.trail)
                else:
                    self.trail.pop(0)

    
    @property
    def velX(self):
        return self._velX

    @velX.setter
    def velX(self,value):
        if(self.velX <= 0 and value >= 0) or (self.velX >= 0 and value <= 0):
            gridW = self.game.MAP_WIDTH // self.game.GRID_X
            gridH = self.game.MAP_HEIGHT // self.game.GRID_Y
            self.x = round(value/gridW) * gridW + 0.5*gridW
            self.y = round(value/gridH) * gridH + 0.5*gridH
            self._velX = value

    @property
    def velY(self):
        return self._velY

    @velY.setter
    def velY(self,value):
        if(self.velY <= 0 and value >= 0) or (self.velY >= 0 and value <= 0):
            gridW = self.game.MAP_WIDTH // self.game.GRID_X
            gridH = self.game.MAP_HEIGHT // self.game.GRID_Y
            self.x = round(value/gridW) * gridW + 0.5*gridW
            self.y = round(value/gridH) * gridH + 0.5*gridH
            self._velY = value


def drawSnake(screen,snake,game):
    snakeColor  = (34,139,34) #forestgreen
    
    x,y,w,h = _computeRect(snake.x,snake.y,game)
    pygame.draw.rect(screen, snakeColor, pygame.Rect(x,y,w,h))
    for cx,cy in snake.trail:
        x,y,w,h    = _computeRect(cx,cy,game)     
        pygame.draw.rect(screen, snakeColor, pygame.Rect(x,y,w,h))

def drawApple(screen,game):
    appleColor = (255,0,0)
    x,y,w,h    = _computeRect(game.appleX,game.appleY,game)
    pygame.draw.rect(screen, appleColor, pygame.Rect(x,y,w,h))

def main():
    game = Game(800,800,80,80)
    
    snakeStart = (game.MAP_WIDTH // (2*game.GRID_X),game.MAP_HEIGHT // (2*game.GRID_Y))
    snake = Snake(game, snakeStart)

    pygame.init()
    screen = pygame.display.set_mode((game.MAP_WIDTH,game.MAP_HEIGHT))
    running = True

    FPS   = 60
    clock = pygame.time.Clock()
    ku,kd,kl,kr = False, False, False, False
    gridW   = game.MAP_WIDTH // game.GRID_X
    gridH   = game.MAP_HEIGHT // game.GRID_Y
    speedX  = gridW / FPS
    speedY  = gridH / FPS
    snake.velX = speedX

    while running:
        startT = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        
        #input
        if pygame.key.get_pressed()[pygame.K_UP]:
            kd,ku,kl,kr = False,True,False,False
        elif pygame.key.get_pressed()[pygame.K_DOWN]:
            kd,ku,kl,kr = True,False,False,False
        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            kd,ku,kl,kr = False,False,True,False
        elif pygame.key.get_pressed()[pygame.K_RIGHT]:
            kd,ku,kl,kr = False,False,False,True
        
        if kd:
            snake.velX = 0
            snake.velY = speedY
        elif ku:
            snake.velX = 0
            snake.velY = -speedY
        elif kl:
            snake.velY = 0
            snake.velX = -speedX
        elif kr:
            snake.velY = 0
            snake.velX = speedX
        


        #update        
        snake.update()
        print(snake.velX,snake.velY)
        #draw
        screen.fill((0,0,0))
        drawSnake(screen,snake,game)           
        drawApple(screen,game)
        

        #blit
        pygame.display.flip()
        clock.tick(FPS)               
        

if __name__ == '__main__':
    main()
