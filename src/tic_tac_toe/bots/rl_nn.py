import pickle
import numpy as np
from torch import nn




class rl_nn:
    def __init__(self, player):
        self.name = 'rl_nn'
        self.player = player
        self.stack = nn.Sequential(
            nn.Linear(18, 36),
            nn.ReLu(),
            nn.Linear(36,36),
            nn.ReLu(),
            nn.Linear(36,9)
        )

        try:
            self.weights = pickle.load(open(self.name + '_weights.p','rb')) # expected_reward = pickle.load(open('milesbot_expected_reward.p','rb'))
        except:
            print('cant find')
    
    def boardToInput(self, board):
        opponent = 'X' if self.player == 'O' else 'O'
        
        board_flat = np.array(board).flatten()
        player_encoding = np.array([1 if cell == self.player else 0 for cell in board_flat])
        opponent_encoding = np.array([1 if cell == opponent else 0 for cell in board_flat])
        
        nn_input = np.concatenate([player_encoding, opponent_encoding])
        
        return nn_input

    def backpropogate(self):
        

    def get_move(self, board):
        pass
        
    def update_reward(self, result):
        pass
    
    def get_state(self, row, col, board):
        pass

