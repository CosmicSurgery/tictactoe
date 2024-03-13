import pickle
import numpy as np



class rl_nn:
    def __init__(self, player):
        self.name = 'rl_nn'
        self.player = player
        try:
            self.weights = pickle.load(open(self.name + '_weights.p','rb')) # expected_reward = pickle.load(open('milesbot_expected_reward.p','rb'))
        except:
            print('cant find')

    def get_move(self, board):
        pass
        
    def update_reward(self, result):
        pass
    
    def get_state(self, row, col, board):
        pass

