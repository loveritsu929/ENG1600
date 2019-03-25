# -*- coding: utf-8 -*-
import pickle
import numpy as np
#dic = {1:'a', 2:'b', 3:'d'}
#with open('./testpickle.test', 'wb') as fp:
#    pickle.dump(dic, fp)
#
#with open('./testpickle', 'rb') as fp:
#    print(type(pickle.load(fp)))

#from gameBackup import SnakeGame
#
#game = SnakeGame()
#game.main()

#q_dict = {}
#with open('./learned_model.mdl', 'rb') as fp:
#    q_dict = pickle.load(fp)
#    print(type(q_dict))
#
#for k,v in q_dict.items():
#    #k: tuple
#    mat = np.array(k).reshape(7,-1)
#    print('Game State: \n', mat, '\nAction values: ', v, '\n')

class testclass():
    
    def __init__(self):
        self.a = 1
        
    def echo(self, line = self.a):
        print(line)
        
tt = testclass()
tt.echo('aaa')
        
    