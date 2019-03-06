# -*- coding: utf-8 -*-

from collections import deque
import torch
import numpy as np
import torch.nn as nn
import random, os

FRAME_PER_ACTION = 1
GAMMA = 0.99 # decay rate of past observations
OBSERVE = 10000 # timesteps to observe before training
EXPLORE = 3000000 # frames over which to anneal epsilon
FINAL_EPSILON = 0.0001 #0.001 # final value of epsilon
INITIAL_EPSILON = 0.1  #0.01 # starting value of epsilon
REPLAY_MEMORY = 100 # number of previous transitions to remember
BATCH_SIZE = 32 # size of minibatch
UPDATE_TIME = 100
width=80
height=80;
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class NNetwork(nn.Module):
    def __init__(self):
        super(NNetwork, self).__init__()
        
        #TODO: CNN structure; init NN
        
    def forward(self, x):
        
        out = x
        return out

class DQN:
    def __init__(self, actions):
        self.loss_func = nn.MSELoss()
    
    def save(self):
        torch.save(self.Q_net.state_dict(), 'params.pth')
        
    def load(self):
        if os.path.exists("params.pth"):
            print("load model param")
            self.Q_net.load_state_dict(torch.load('params.pth'))
            self.Q_netT.load_state_dict(torch.load('params.pth'))
            
    def train(self):
        #TODO
        return
    def setPerception(self,nextObservation,action,reward,terminal):
        #TODO
        return
    def getAction(self):
        #TODO
        return
    def setInitState(self, observation):
        self.currentState = np.stack((observation, observation, observation, observation), axis=0)
        print(self.currentState.shape)  