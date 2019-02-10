# -*- coding: utf-8 -*-
'''
ENG 1600: Smart Snake Game
the RL agent class
'''

import numpy as np
import torch
import torch.nn as nn
import pickle, os, time
import mySnake
from mySnake import SnakeGame

model_file = './learned_model.mdl'

EPSILON = 0.7 # Prob. of exploit learned rules
ALPHA = 0.1 # RL learning rate
BETA = -0.5 # penalty factor for ending early
GAMMA = 0.9 # discount factor for future reward

class SimpleAgent(object):
    # A simple for a 5x5 game
    ACTIONS = [SnakeGame.UP, SnakeGame.DOWN, SnakeGame.LEFT, SnakeGame.RIGHT]
    # n_states <= 2 .^ 25 ~ 33.5 MBytes ==> ca be stored in a dict
    
    def __init__(self):
        self.game = mySnake.SnakeGame()
        self.q_dict = {} # {game_state: ndarray [Q-values for actions]}
    
    def manhattan(self):
        return abs(self.game.food['x']-self.game.snake_body[0]['x']) + abs(self.game.food['y']-self.game.snake_body[0]['y'])
    
    def mat_to_tuple(self, mat):
        if isinstance(mat, np.ndarray):
            return tuple(mat.reshape(1,-1)[0])
        else:
            print('not a ndarray!')
    
    def lookup_dict(self, state):
        if state in self.q_dict:
            q_array = self.q_dict[state]
        else:
            q_array = np.array([0.0, 0.0, 0.0, 0.0])
            self.q_dict[state] = q_array
        
        return q_array

    def choose_action(self):
        state = self.mat_to_tuple(self.game.get_game_board())
        if (np.random.uniform() > EPSILON):
            action = np.random.choice(SimpleAgent.ACTIONS)
        else:
            #action = self.q_dict[state].argmax()
            action = self.lookup_dict(state).argmax()
        q_array = self.lookup_dict(state) #self.q_dict[state][action]
        return state, action, q_array[action] 
            
    def get_reward(self, terminated):
        #new_state = tuple(self.game.get_game_board.reshape(1,-1)[0])
        new_len = len(self.game.snake_body)
        new_manhattan = self.manhattan()
        
        if terminated:
            R = self.game.score + BETA * (self.game.maxScore - self.game.score) # may be negative
        else:
            R = (new_manhattan - self.prev_manhattan) + 10 * (new_len - self.prev_len)
            
        return R
    
    def play(self):
        # play 'ep' times
        print("start to play")
        for epoch in range(10):
            terminated = False
            alreadyStarted = False
            # load the learned model
            if os.path.isfile(model_file):
                with open(model_file, 'rb') as fp:
                    self.q_dict = pickle.load(fp)
            
            # play the game
            while not terminated:
                #time.sleep(1)
                print(' ')
                prev_state, A, prev_Q = self.choose_action()
                print('choose A')
                self.prev_state = prev_state
                self.prev_len = len(self.game.snake_body)
                self.prev_manhattan = self.manhattan()
                # choose action A, play a step
                self.game.control(A)
                self.game.can_play()
                
                # allow to restart
                self.game.can_restart()
                
                
                if not alreadyStarted:
                    # stuck in this loop
                    self.game.main()
                    alreadyStarted = True
                else:
                    self.game.play_one_step()
                print('play a step : action A')
                new_state = tuple(self.game.get_game_board().reshape(1,-1)[0])
                
                # get feedback
                terminated = not self.game.alive
                R = self.get_reward(terminated)
                
                
                
                # Q <-- Q + alpha* (R + gamma*max_future_Q - Q)
                target_Q = R + GAMMA * self.lookup_dict(new_state).max()
                self.q_dict[prev_state][A] += ALPHA * (target_Q - prev_Q)
                
                
                
            print('finish one epoch')
            with open(model_file, 'wb') as fp:
                pickle.dump(self.q_dict, fp)
                
if __name__ == '__main__':
    agent = SimpleAgent()
    agent.play()
        