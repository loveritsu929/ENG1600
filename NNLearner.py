# -*- coding: utf-8 -*-
import random, copy
import time
import pygame
import sys
import numpy as np
from pygame.locals import *
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import models
from smartSnake import PFSnake

model = models.vgg16_bn(pretrained=True)
model.classifier = torch.nn.Sequential(torch.nn.Linear(25088, 4096),
                                       torch.nn.ReLU(),
                                       torch.nn.Dropout(p=0.5),
                                       torch.nn.Linear(4096, 4096),
                                       torch.nn.ReLU(),
                                       torch.nn.Dropout(p=0.5),
                                       torch.nn.Linear(4096, 4))
criterion = nn.CrossEntropyLoss()  
lnR = 1e-3 
batchSize = 32
optimizer = optim.Adam(model.parameters(), lr = lnR, amsgrad = True)

# like collate_fn in Dataloader; turn a list of samples to tensors
def my_collate(batch):
    boards = [torch.as_tensor(item[0]) for item in batch]
    boards = torch.stack(boards)
    moves = [item[1] for item in batch]
    moves = torch.LongTensor(moves)
    return [boards, moves]

def train(model, criterion, optimizer, batch):
    # batch: a list of batchSize (board, move)
    running_loss = 0
    running_corrects = 0
    sample, label = my_collate(batch)
    out = model(sample)
    loss = criterion(out, label)
    
    #update
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    #stats
    _, preds = torch.max(out, 1) 
    running_loss += loss.item() * sample.size(0)
    running_corrects += torch.sum(preds == label.data)
    
    print("Train one mini-batch: Loss={:.4f}, Acc={:.4f}".format(
            running_loss, running_corrects.double()/sample.size(0)))
    
    return

class OracleSnake(PFSnake):    
    def __init__(self):
        pygame.init()
        self.speed = 20
        self.speed_clock = pygame.time.Clock()
        self.score = 0
        self.ate = 0
        self.maxScore = PFSnake.board_height * PFSnake.board_width * 10
        self.alive = True
        
        # NN part
        self.model = model
        self.criterion = criterion
        self.optimizer = optimizer
        
        #temporary vars; for path finding
        self.tmp_board = np.zeros((PFSnake.board_height, PFSnake.board_width))
        self.board_dataset = [None]*batchSize
        self.dataset_index = 0
        self.initialize()
        
    def PFPlay(self):
        self.reset_board(self.tmp_board, self.snake_body)
        move = -1
        found = self.update_board(self.tmp_board,self.snake_body)
        board = copy.deepcopy(self.tmp_board)
        print(board)
        if found:
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
        #print('move == {:d}'.format(move))
        print(self.dataset_index)
        if self.dataset_index < 31:
            self.board_dataset[self.dataset_index] = (board, move)
            self.dataset_index += 1
        else:
            # train one mini-batch
            train(self.model, self.criterion, self.optimizer, self.board_dataset)
            
            self.dataset_index = 0
            self.board_dataset = [None]*batchSize
            self.board_dataset[self.dataset_index] = (board, move)
            self.dataset_index += 1
    

if __name__ == '__main__':
    # need to change the game size first.(VGG input 224*224)
    game = OracleSnake()
    game.main()
