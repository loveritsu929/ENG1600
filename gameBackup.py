# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
"""
ENG 1600

for human player
"""

import random
import time
import pygame
import sys
import numpy as np
from pygame.locals import *



class SnakeGame(object):
    # class attributes
    # a 50x50 gameboard
    window_height = 1000
    window_width = 1000
    cell_size = 20
    board_height = int(window_height/cell_size) #5 10 20
    board_width = int(window_width/cell_size)  # 5 10 20

    # define the colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    gray = (40, 40, 40)
    green = (0, 255, 0)
    blue = (0, 0, 255)

    # define the directions
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    
    def __init__(self):
        pygame.init()
        self.speed = 15
        self.speed_clock = pygame.time.Clock()
        self.score = 0
        self.maxScore = SnakeGame.board_height * SnakeGame.board_width * 10
        self.alive = True

    
    def restart(self):
        time.sleep(1)
        self.score = 0
        self.alive = True
        #self.run() #  or main()
    
    def main(self):
        self.screen = pygame.display.set_mode((SnakeGame.window_width, SnakeGame.window_height))
        self.screen.fill(SnakeGame.white)
        pygame.display.set_caption("ENG 1600: SmartSnake")
        
        while True:
            self.run()
            print('Got Score: ', self.score)
            if True:
                self.restart()
		#show_gameover_info
    
    def run(self):
        # start from the center
        init_x = int(SnakeGame.board_width/2)
        init_y = int(SnakeGame.board_height/2)
        
        self.snake_body = [{'x':init_x, 'y':init_y},
                           {'x':init_x-1, 'y':init_y},
                           {'x':init_x-2, 'y':init_y}]
        self.direction = SnakeGame.RIGHT
        
        self.food = self.generate_food() # random food location
        
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    #self.restart()
                elif event.type == KEYDOWN:
                    if event.key == K_LEFT and self.direction != SnakeGame.RIGHT:
                        self.direction = SnakeGame.LEFT
                    elif event.key == K_RIGHT and self.direction != SnakeGame.LEFT:
                        self.direction = SnakeGame.RIGHT
                    elif event.key == K_UP and self.direction != SnakeGame.DOWN:
                        self.direction = SnakeGame.UP
                    elif event.key == K_DOWN and self.direction != SnakeGame.UP:
                        self.direction = SnakeGame.DOWN
                        
            self.move_snake()
            self.alive = self.check_alive()
            
            if not self.alive:
                break
            
            self.check_food()
            #print(self.get_game_board())
            self.score = (len(self.snake_body) - 3) * 10
            self.draw_game()
            
            pygame.display.update()
            self.speed_clock.tick(self.speed)
        
    def generate_food(self):
        Loc = {'x': random.randint(0, SnakeGame.board_width - 1), 'y': random.randint(0, SnakeGame.board_height - 1)}
        while Loc in self.snake_body:
            Loc = {'x': random.randint(0, SnakeGame.board_width - 1), 'y': random.randint(0, SnakeGame.board_height - 1)}
            
        return Loc  
    
    def move_snake(self):
        if self.direction == SnakeGame.UP:
            newHead = {'x': self.snake_body[0]['x'], 'y': self.snake_body[0]['y'] - 1}
        elif self.direction == SnakeGame.DOWN:
            newHead = {'x': self.snake_body[0]['x'], 'y': self.snake_body[0]['y'] + 1}
        elif self.direction == SnakeGame.LEFT:
            newHead = {'x': self.snake_body[0]['x'] - 1, 'y': self.snake_body[0]['y']}
        elif self.direction == SnakeGame.RIGHT:
            newHead = {'x': self.snake_body[0]['x'] + 1, 'y': self.snake_body[0]['y']}

        self.snake_body.insert(0, newHead)
    
    def check_alive(self):
        alive = True
        if self.snake_body[0]['x'] == -1 or \
        self.snake_body[0]['x'] == SnakeGame.board_width or \
        self.snake_body[0]['y'] == -1 or \
		self.snake_body[0]['y'] == SnakeGame.board_height:
            alive = False
                
        for node in self.snake_body[1:]:
            if node['x'] == self.snake_body[0]['x'] and \
            node['y'] == self.snake_body[0]['y']:
                alive = False
                break
        
        return alive
        
    def check_food(self):
        if self.snake_body[0]['x'] == self.food['x'] and self.snake_body[0]['y'] == self.food['y']:
            self.food = self.generate_food()
        else:
            self.snake_body.pop(-1)
        
    def draw_game(self):
        self.screen.fill(SnakeGame.black)
        #draw grid
        for x in range(0, SnakeGame.window_width, SnakeGame.cell_size):
            pygame.draw.line(self.screen, SnakeGame.gray, (x, 0), (x, SnakeGame.window_height))
        for y in range(0, SnakeGame.window_height, SnakeGame.cell_size):
            pygame.draw.line(self.screen, SnakeGame.gray, (0, y), (SnakeGame.window_width, y))
        
        #draw snake
        headx = self.snake_body[0]['x'] * SnakeGame.cell_size
        heady = self.snake_body[0]['y'] * SnakeGame.cell_size
        pygame.draw.rect(self.screen, SnakeGame.green, pygame.Rect(headx, heady, SnakeGame.cell_size, SnakeGame.cell_size))
        for node in self.snake_body[1:]:
            x = node['x'] * SnakeGame.cell_size
            y = node['y'] * SnakeGame.cell_size
            pygame.draw.rect(self.screen, SnakeGame.blue, pygame.Rect(x, y, SnakeGame.cell_size, SnakeGame.cell_size))
        
        #draw food
        x = self.food['x'] * SnakeGame.cell_size
        y = self.food['y'] * SnakeGame.cell_size
        pygame.draw.rect(self.screen, SnakeGame.red, pygame.Rect(x, y, SnakeGame.cell_size, SnakeGame.cell_size))
        
        #draw score
        font = pygame.font.SysFont('arial', 20)
        scoreSurf = font.render('Score: %s' % self.score, True, SnakeGame.white)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (int(SnakeGame.window_width / 2) - 20, 10)
        self.screen.blit(scoreSurf, scoreRect)
        
    def get_game_board(self):
        #in RL agent, turn it to a tuple to make it hashable
        mat = np.zeros((self.board_height, self.board_width))
        mat[self.food['y']][self.food['x']] = 2
        for node in self.snake_body:
            # notice the order!!!!
            mat[node['y']][node['x']] = 1
        
        return mat
    
    #def terminate(self):
if __name__ == '__main__':
    game = SnakeGame()
    game.main()