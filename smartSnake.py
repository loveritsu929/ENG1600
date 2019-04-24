# -*- coding: utf-8 -*-
"""
ENG 1600

the path-finding snake
"""

import random
import time
import pygame
import sys
import numpy as np
from pygame.locals import *


class PFSnake(object):
    # class attributes
    # a 50x50 gameboard
    window_height = 100 #400
    window_width = 100 #400
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
    
    #board element
    FOOD = 0
    UNDEF = (board_height + 1) * (board_width + 1)
    SNAKE = 2 * UNDEF

    
    def __init__(self):
        pygame.init()
        self.speed = 5
        self.speed_clock = pygame.time.Clock()
        self.score = 0
        self.ate = 0
        self.maxScore = PFSnake.board_height * PFSnake.board_width * 10
        self.alive = True
        
        #temporary vars; for path finding
        self.tmp_board = np.zeros((PFSnake.board_height, PFSnake.board_width))
        
        self.initialize()
        
    def initialize(self):
        # start from the center
        init_x = int(PFSnake.board_width/2)
        init_y = int(PFSnake.board_height/2)
        
        self.snake_body = [{'x':init_x, 'y':init_y},
                           {'x':init_x-1, 'y':init_y},
                           {'x':init_x-2, 'y':init_y}]
        #self.direction = PFSnake.RIGHT
        
        self.food = self.generate_food() # random food location
    
    def restart(self):
        time.sleep(1)
        self.score = 0
        self.ate = 0
        self.alive = True
        self.initialize()  
    
    def main(self):
        while True:
            self.run()
            self.restart()
            
    def run(self):
        self.screen = pygame.display.set_mode((PFSnake.window_width, PFSnake.window_height))
        self.screen.fill(PFSnake.white)
        pygame.display.set_caption("ENG 1600: SmartSnake")
        
#        while not stopPlay:
        while self._check_alive():
            print('PFPlay')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            self.PFPlay()
            print('Played one step')
            self.draw_game()
            pygame.display.update()
            self.speed_clock.tick(self.speed)
        print('Got Score: ', self.score)
    
    def PFPlay(self):
        self.reset_board(self.tmp_board, self.snake_body)
        move = -1
        if self.update_board(self.tmp_board,self.snake_body):
            #find path between food and head
            move = self.find_path()
        else:
            move = self.follow_tail()
        
        if move == -1:
            move = self.just_one_possible_move()
        
        if move != -1:
            self.move_snake(move)
        else:
            return False
        print('move == {:d}'.format(move))
        return False
        
        
#    def play_one_step(self):
#        print('Snake game: do action A')
#        for event in pygame.event.get():
#            if event.type == QUIT:
#                pygame.quit()
#                sys.exit()
#                   
#        self.move_snake()
#        self.alive = self.check_alive()
#            
#        self.check_food()
#        self.score = self.ate*10 #(len(self.snake_body) - 3) * 10
#        self.draw_game()
#            
#        pygame.display.update()
#        self.speed_clock.tick(self.speed)
#        print(self.get_game_board(), '\n')
        
    def is_valid_move(self, direction):
        assert direction in [0,1,2,3]
        valid = direction == PFSnake.UP and self.direction != PFSnake.DOWN or \
        direction == PFSnake.DOWN and self.direction != PFSnake.UP or \
        direction == PFSnake.LEFT and self.direction != PFSnake.RIGHT or \
        direction == PFSnake.RIGHT and self.direction != PFSnake.LEFT
        return valid
    
    def is_cell_free(self, cell):
        return not (cell in self.snake_body)
    
    def generate_food(self):
        Loc = {'x': random.randint(0, PFSnake.board_width - 1), 'y': random.randint(0, PFSnake.board_height - 1)}
        while Loc in self.snake_body:
            Loc = {'x': random.randint(0, PFSnake.board_width - 1), 'y': random.randint(0, PFSnake.board_height - 1)}
            
        return Loc  
    
    def is_move_possible(self, cell, direction):
        flag = False
        nextCell = self.move_cell(cell,direction)
        
        if direction == PFSnake.LEFT:
            flag = True if cell['x'] > 0 else False
        elif direction == PFSnake.RIGHT:
            flag = True if cell['x'] < PFSnake.board_width-1 else False
        elif direction == PFSnake.UP:
            flag = True if cell['y'] > 0 else False
        elif direction == PFSnake.DOWN:
            flag = True if cell['y'] < PFSnake.board_height-1 else False
            
        if nextCell in self.snake_body[1:]:
            flag = False
        
        return flag
           
    def move_virtual_snake(self, direction, snake):
        print(direction)
        if direction == -1:
            direction = random.randint(0,3)
        if direction == PFSnake.UP:
            newHead = {'x': snake[0]['x'], 'y': snake[0]['y'] - 1}
        elif direction == PFSnake.DOWN:
            newHead = {'x': snake[0]['x'], 'y': snake[0]['y'] + 1}
        elif direction == PFSnake.LEFT:
            newHead = {'x': snake[0]['x'] - 1, 'y': snake[0]['y']}
        elif direction == PFSnake.RIGHT:
            newHead = {'x': snake[0]['x'] + 1, 'y': snake[0]['y']}

        self.snake_body.insert(0, newHead)
        
        
        
    def move_snake(self, direction):
#        # if end, do nothing
#        if not self.check_alive():
#            return
        if direction == PFSnake.UP:
            newHead = {'x': self.snake_body[0]['x'], 'y': self.snake_body[0]['y'] - 1}
        elif direction == PFSnake.DOWN:
            newHead = {'x': self.snake_body[0]['x'], 'y': self.snake_body[0]['y'] + 1}
        elif direction == PFSnake.LEFT:
            newHead = {'x': self.snake_body[0]['x'] - 1, 'y': self.snake_body[0]['y']}
        elif direction == PFSnake.RIGHT:
            newHead = {'x': self.snake_body[0]['x'] + 1, 'y': self.snake_body[0]['y']}

        self.snake_body.insert(0, newHead)
        return self._check_food()
        
    def move_cell(self, cell, direction):
        if direction == PFSnake.UP:
            newCell = {'x': cell['x'], 'y': cell['y'] - 1}
        elif direction == PFSnake.DOWN:
            newCell = {'x': cell['x'], 'y': cell['y'] + 1}
        elif direction == PFSnake.LEFT:
            newCell = {'x': cell['x'] - 1, 'y': cell['y']}
        elif direction == PFSnake.RIGHT:
            newCell = {'x': cell['x'] + 1, 'y': cell['y']}
            
        return newCell
    
    def _check_alive(self):
        alive = False
        # if there is a empty cell near s_head, return true
        head = self.snake_body[0]
        for direction in [0,1,2,3]:
            if self.is_move_possible(head, direction):
                alive = True
                break
#        if self.snake_body[0]['x'] == -1 or \
#        self.snake_body[0]['x'] == PFSnake.board_width or \
#        self.snake_body[0]['y'] == -1 or \
#		self.snake_body[0]['y'] == PFSnake.board_height:
#            alive = False
#                
#        for node in self.snake_body[1:]:
#            if node['x'] == self.snake_body[0]['x'] and \
#            node['y'] == self.snake_body[0]['y']:
#                alive = False
#                break
        return alive
        
    def _check_food(self):
        ate = False
        # if end, do nothing
        if not self._check_alive():
            return
        if self.snake_body[0]['x'] == self.food['x'] and self.snake_body[0]['y'] == self.food['y']:
            self.food = self.generate_food()
            self.ate += 1
            ate = True
        else:
            self.snake_body.pop(-1)
        return ate
        
    def draw_game(self):
        self.screen.fill(PFSnake.black)
        #draw grid
        for x in range(0, PFSnake.window_width, PFSnake.cell_size):
            pygame.draw.line(self.screen, PFSnake.gray, (x, 0), (x, PFSnake.window_height))
        for y in range(0, PFSnake.window_height, PFSnake.cell_size):
            pygame.draw.line(self.screen, PFSnake.gray, (0, y), (PFSnake.window_width, y))
        
        #draw snake
        headx = self.snake_body[0]['x'] * PFSnake.cell_size
        heady = self.snake_body[0]['y'] * PFSnake.cell_size
        pygame.draw.rect(self.screen, PFSnake.green, pygame.Rect(headx, heady, PFSnake.cell_size, PFSnake.cell_size))
        for node in self.snake_body[1:]:
            x = node['x'] * PFSnake.cell_size
            y = node['y'] * PFSnake.cell_size
            pygame.draw.rect(self.screen, PFSnake.blue, pygame.Rect(x, y, PFSnake.cell_size, PFSnake.cell_size))
        
        #draw food
        x = self.food['x'] * PFSnake.cell_size
        y = self.food['y'] * PFSnake.cell_size
        pygame.draw.rect(self.screen, PFSnake.red, pygame.Rect(x, y, PFSnake.cell_size, PFSnake.cell_size))
        
        #draw score
#        font = pygame.font.SysFont('arial', 20)
#        scoreSurf = font.render('Score: %s' % self.score, True, PFSnake.white)
#        scoreRect = scoreSurf.get_rect()
#        scoreRect.topleft = (int(PFSnake.window_width / 2) - 20, 10)
#        self.screen.blit(scoreSurf, scoreRect)
    
    # reset board after update_board  
    def reset_board(self, board, snake):
        #board = self.tmp_board
        for row in range(PFSnake.board_height):
            for col in range(PFSnake.board_width):
                board[row][col] = PFSnake.UNDEF
        
        board[self.food['y']][self.food['x']] = PFSnake.FOOD
        
        for node in snake:
            board[node['y']][node['x']] = PFSnake.SNAKE
    
    # compute the distance to food for every non-snake cell
    def update_board(self, board, snake):
        found = False      
        queue = []
        queue.append(self.food)
        visited = np.zeros((PFSnake.board_height, PFSnake.board_width))
        while len(queue)!=0:
            cell = queue.pop(0)
            if visited[cell['y']][cell['x']]==1:
                continue
            visited[cell['y']][cell['x']]=1
            for direction in range(4):
                if self.is_move_possible(cell,direction):
                    newCell = self.move_cell(cell,direction)
                    if newCell==snake[0]:
                        # found head
                        found = True
                    if board[newCell['y']][newCell['x']] < PFSnake.SNAKE:
                        if board[newCell['y']][newCell['x']] > \
                        board[cell['y']][cell['x']] + 1:
                            board[newCell['y']][newCell['x']] = \
                            board[cell['y']][cell['x']] + 1
                        if visited[newCell['y']][newCell['x']] == 0:
                            queue.append(newCell)
#        print('board updated')
#        print(board)
        return found

    def get_shortest_safe_move(self, board, snake):
        move = -1
        min = PFSnake.SNAKE
        self.reset_board(board, snake)
        self.update_board(board, snake)
        for direction in range(4):
            if self.is_move_possible(snake[0], direction):
                nextHead = self.move_cell(snake[0], direction)
                if board[nextHead['y']][nextHead['x']] < min:
                    min = board[nextHead['y']][nextHead['x']]
                    move = direction
                
        return move
    
    def get_longest_safe_move(self, board):
        move = -1
        max = -1
        self.reset_board(self.tmp_board, self.snake_body)
        self.update_board(self.tmp_board,self.snake_body)
        for direction in range(4):
            if self.is_move_possible(self.snake_body[0], direction):
                nextHead = self.move_cell(self.snake_body[0], direction)
                if board[nextHead['y']][nextHead['x']] > max and \
                board[nextHead['y']][nextHead['x']] < PFSnake.UNDEF:
                    max = board[nextHead['y']][nextHead['x']]
                    move = direction
            
        return move
    
    def can_find_tail(self):
        self.reset_board(self.tmp_board, self.snake_body)
        temp = self.tmp_board
        tail = self.snake_body[-1]
        temp[tail['y']][tail['x']] = PFSnake.FOOD
        temp[self.food['y']][self.food['x']] = PFSnake.SNAKE
        
        result = self.update_board(self.tmp_board,self.snake_body)
        for direction in range(4):
            if self.is_move_possible(self.snake_body[0], direction):
                newHead = self.move_cell(self.snake_body[0], direction)
                if newHead == self.snake_body[-1] and len(self.snake_body) >3:
                    # cannot follow tail if tail is next to head
                    result = False
        return result
    
    def follow_tail(self):
        self.reset_board(self.tmp_board, self.snake_body)
        temp = self.tmp_board
        tail = self.snake_body[-1]
        temp[tail['y']][tail['x']] = PFSnake.FOOD
        temp[self.food['y']][self.food['x']] = PFSnake.SNAKE
        
        self.update_board(self.tmp_board,self.snake_body)
        temp[tail['y']][tail['x']] = PFSnake.SNAKE
    
        return self.get_longest_safe_move(self.tmp_board)
    
    def just_one_possible_move(self):
        move = -1
        self.reset_board(self.tmp_board, self.snake_body)
        self.update_board(self.tmp_board,self.snake_body)
        min = PFSnake.SNAKE
        
        for direction in range(4):
            if self.is_move_possible(self.snake_body[0], direction):
                nextHead = self.move_cell(self.snake_body[0], direction)
                if self.tmp_board[nextHead['y']][nextHead['x']] < min:
                    min = self.tmp_board[nextHead['y']][nextHead['x']]
                    move = direction
        
        return move
    
    # let a virtual snake try to find path
    def virtual_move(self):
        temp = self.tmp_board.copy()
        snake_backup = self.snake_body.copy()
        virtual_snake = self.snake_body.copy()
        self.reset_board(temp, virtual_snake)
        food_ate = False
        
        while not food_ate:
            print('in virtual move')
            # TODO: impl api for virtual snake
            self.update_board(temp, virtual_snake)
            move = self.get_shortest_safe_move(temp, virtual_snake)
            food_ate = self.move_virtual_snake(move, virtual_snake)
        
        self.snake_body = snake_backup
        self.reset_board(self.tmp_board, self.snake_body)            
        return
    
    def find_path(self):
        #self.virtual_move()
        if self.can_find_tail():
            return self.get_shortest_safe_move(self.tmp_board, self.snake_body)
        else:
            return self.follow_tail()

if __name__ == '__main__':
    game = PFSnake()
    game.main()
