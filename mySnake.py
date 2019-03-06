# -*- coding: utf-8 -*-
"""
ENG 1600

the snake game class
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
    window_height = 100
    window_width = 100
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
        self.speed = 1
        self.speed_clock = pygame.time.Clock()
        self.score = 0
        self.ate = 0
        self.maxScore = SnakeGame.board_height * SnakeGame.board_width * 10
        self.alive = True
        self.canPlay = True
        self.canRestart = True
        self.initialize()
#        print('init state: ')
        print('Init: \n', self.get_game_board(),'\n')
        
    def initialize(self):
        # start from the center
        init_x = int(SnakeGame.board_width/2)
        init_y = int(SnakeGame.board_height/2)
        
        self.snake_body = [{'x':init_x, 'y':init_y},
                           {'x':init_x-1, 'y':init_y},
                           {'x':init_x-2, 'y':init_y}]
        self.direction = SnakeGame.RIGHT
        
        self.food = self.generate_food() # random food location
    
    def restart(self):
        time.sleep(1)
        self.score = 0
        self.ate = 0
        self.alive = True
        self.initialize()
        
    
    def main(self):
        self.screen = pygame.display.set_mode((SnakeGame.window_width, SnakeGame.window_height))
        self.screen.fill(SnakeGame.white)
        pygame.display.set_caption("ENG 1600: SmartSnake")
        
        self.play_one_step()
        
        if True and not self.alive:
#       if self.canRestart:
            print('Got Score: ', self.score, 'isAlive: ', self.alive)
            self.restart()
#       else:
#           pygame.quit()
#           sys.exit()
		#show_gameover_info
    
    #like a mutex lock
    def can_play(self):
        self.canPlay = True  
        
    def can_restart(self):
        self.canRestart = True
    
    def play_one_step(self):
        print('Snake game: do action A')
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                #self.restart()
#            elif event.type == KEYDOWN:
#                if event.key == K_LEFT and self.direction != SnakeGame.RIGHT:
#                    self.direction = SnakeGame.LEFT
#                elif event.key == K_RIGHT and self.direction != SnakeGame.LEFT:
#                    self.direction = SnakeGame.RIGHT
#                elif event.key == K_UP and self.direction != SnakeGame.DOWN:
#                    self.direction = SnakeGame.UP
#                elif event.key == K_DOWN and self.direction != SnakeGame.UP:
#                    self.direction = SnakeGame.DOWN
        
        #TODO: restrictions for rlagent
                   
        self.move_snake()
        self.alive = self.check_alive()
            
        self.canPlay = False # wait for agent to play
        self.canRestart = False
            
        time.sleep(1)
            
        if not self.alive:
            print('end')
            
        self.check_food()
        #print(self.get_game_board())
        self.score = self.ate*10 #(len(self.snake_body) - 3) * 10
        self.draw_game()
            
        pygame.display.update()
        self.speed_clock.tick(self.speed)
        print(self.get_game_board(), '\n')
        
    #control method for the rl agent
    def control(self, direction):
        assert direction in [0,1,2,3]
        if direction == SnakeGame.UP and self.direction != SnakeGame.DOWN or \
        direction == SnakeGame.DOWN and self.direction != SnakeGame.UP or \
        direction == SnakeGame.LEFT and self.direction != SnakeGame.RIGHT or \
        direction == SnakeGame.RIGHT and self.direction != SnakeGame.LEFT:
            self.direction = direction
        else:
            print('Do nothing')
        
    def generate_food(self):
        Loc = {'x': random.randint(0, SnakeGame.board_width - 1), 'y': random.randint(0, SnakeGame.board_height - 1)}
        while Loc in self.snake_body:
            Loc = {'x': random.randint(0, SnakeGame.board_width - 1), 'y': random.randint(0, SnakeGame.board_height - 1)}
            
        return Loc  
    
    def move_snake(self):
        # if end, do nothing
        if not self.check_alive():
            return
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
        # if end, do nothing
        if not self.check_alive():
            return
        if self.snake_body[0]['x'] == self.food['x'] and self.snake_body[0]['y'] == self.food['y']:
            self.food = self.generate_food()
            self.ate += 1
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
        #game is n*n ==> state is (n+1)*(n+1)
        #mat = np.zeros((self.board_height+2, self.board_width+2))
        #mat[self.food['y']+1][self.food['x']+1] = 3
        #head = self.snake_body[0]
        #mat[head['y']+1][head['x']+1] = 2
        #for node in self.snake_body[1:]:
            # notice the order!!!!
            #mat[node['y']+1][node['x']+1] = 1
        
        #return mat
        mat = np.zeros((self.board_height, self.board_width))
        if self.alive == False:
            return mat
        mat[self.food['y']][self.food['x']] = 3
        head = self.snake_body[0]
        mat[head['y']][head['x']] = 2
        for node in self.snake_body[1:]:
            # notice the order!!!!
            mat[node['y']][node['x']] = 1
        
        return mat
    
    #def terminate(self):
if __name__ == '__main__':
    game = SnakeGame()
    game.main()
