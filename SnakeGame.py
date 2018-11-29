import pygame
import random

class Game:
    def __init__(self,width,height,(appleX,appleY)):
        self.MAP_WIDTH  = width
        self.MAP_HEIGHT = height
        self.appleX = appleX
        self.appleY = appleY

    def randomApple(self,snakeTrail):
        self.appleX = random.randint(0,self.MAP_WIDTH - 1)
        self.appleY = random.randint(0,self.MAP_HEIGHT - 1)

        while (self.appleX,self.appleY) in snakeTrail:
            self.appleX = random.randint(0,self.MAP_WIDTH - 1)
            self.appleY = random.randint(0,self.MAP_HEIGHT - 1)


class Snake:
    def __init__(self,game):
        self.game            = game
        self.x, self.y       = 0,0
        self.velX, self.velY = 0,0
        self.trail           = []
        self.alive           = True


    def update(self):
        self.trail.append((self.x,self.y))

        self.x = (self.x + self.velX)
        self.y = (self.y + self.velY)

        for x,y in self.trail:
            if self.x == x and self.y == y:
                self.alive = False

        x,y = (self.x, self.y)
        if x < 0 or y < 0 or x >= self.game.MAP_WIDTH or y >= self.game.MAP_HEIGHT:
            self.alive = False

        if not (x == self.game.appleX and y == self.game.appleY):
            self.trail.pop(0)
        else:
            self.game.randomApple(self.trail)



def main():
    game  = Game(400,200,(200,100))
    snake = Snake()

    pygame.init()
    screen = pygame.display.set_mode(,300))
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False



        pygame.display.flip()


if __name__ == '__main__':
    main()
