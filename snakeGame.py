import numpy as np
import sys
import pygame
import random
import time
import multiprocessing


class snakeGame:
    def __init__(self, width=1000, height=1000, nxC=40, nyC=40):
        self.screen = pygame.display.set_mode((height, width))
        self.dimCW = width/nxC
        self.dimCH = height/nyC
        self.bg_color = (25,25,25)
        self.nxC = nxC
        self.nyC = nyC
        self.board = np.zeros((self.nyC, self.nxC))
        self.food = (random.randint(0, self.nyC-1), random.randint(0, self.nxC-1))
        self.sneak = [(random.randint(0, self.nyC-1), random.randint(0, self.nxC-1))]
        self.direction = [0,0]
        self.speed = 0.1
        self.clock = pygame.time.Clock()
        self.FPS = 14
        self.game_over = 0

    def draw_board(self):
        self.screen.fill(self.bg_color)
        for y in range(0, self.nxC):
            for x in range(0, self.nyC):

                poly = [((x)*self.dimCW, (y)*self.dimCH),
                        ((x+1)*self.dimCW, (y)*self.dimCH),
                        ((x+1)*self.dimCW, (y+1)*self.dimCH),
                        ((x)*self.dimCW, (y+1)*self.dimCH)]


                if (y, x) == self.food:
                    pygame.draw.polygon(self.screen, (202, 0, 42), poly)
                elif (y, x) in self.sneak:
                    pygame.draw.polygon(self.screen, (0, 176, 24), poly)
                else:
                    pygame.draw.polygon(self.screen, (128,128,128), poly, 1)
    

    def checkGameOver(self):
        if self.sneak[-1] in self.sneak[:-1]:
            return 1
        if self.sneak[-1][0] >= self.nyC or self.sneak[-1][0] < 0:
            return 1
        if self.sneak[-1][1] >= self.nxC or self.sneak[-1][1] < 0:
            return 1
        return 0
    

    def updateDirection(self):
        pygame.event.pump()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_DOWN]:
            self.direction = [1, 0]
        elif keys[pygame.K_UP]:
            self.direction = [-1, 0]
        elif keys[pygame.K_LEFT]:
            self.direction = [0, -1]
        elif keys[pygame.K_RIGHT]:
            self.direction = [0, 1]


    def game(self):
        while not self.game_over:
            new_pos = (self.sneak[-1][0]+self.direction[0], self.sneak[-1][1]+self.direction[1])
            if self.food == self.sneak[-1]:
                self.sneak.append(new_pos)
                self.food = (random.randint(0, self.nyC-1), random.randint(0, self.nxC-1))
            else:
                for i in range(len(self.sneak)-1):
                    self.sneak[i] = self.sneak[i+1]
                self.sneak[-1] = new_pos
            
            self.updateDirection()
            self.game_over = self.checkGameOver()
            self.draw_board()
            pygame.display.flip()
            self.clock.tick(self.FPS)
