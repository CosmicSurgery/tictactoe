import random
import pickle
import os
import numpy as np
import copy



class tab_q:
    def __init__(self, player):
        self.name = 'tab_q'
        self.epsilon = 0.005
        self.games_played = 0
        self.max_games = 1000
        self.alpha = 0.1
        self.expected_reward = {}
        self.player = player
        self.states = []
        self.moves = []
        self.boards = []
        self.gamma = 0.9

        try:
            self.expected_reward = pickle.load(open(self.name + '_expected_reward.p','rb')) # expected_reward = pickle.load(open('milesbot_expected_reward.p','rb'))
        except Exception as error:
            print('cant find: ', error)
        try:
            self.games_played = pickle.load(open(self.name + '_games_played.p','rb'))
        except Exception as error:
            print('new bot: ', error)

    def get_move(self, board):
        # Generate a random move
        empty_cells = [(row, col) for row in range(3) for col in range(3) if board[row][col] == 0]
        state = self.q_state(board)
        if state in list(self.expected_reward.keys()):
            q = self.expected_reward[state]
        else:
            q = [0 for k in range(9)]
        
        if empty_cells:
            if random.uniform(0,1) < np.e**(-self.epsilon*self.games_played) and self.games_played < self.max_games:
                return random.choice(empty_cells)
            
            move = empty_cells[np.argmax(q)]
        else:
            move = None  # No valid moves available (board is full or already won)
        self.expected_reward[state] = q
        self.boards.append(copy.deepcopy(board))
        self.moves.append(move)

        return move

    def q_state(self, board):
        new_board = np.array(board)
        new_board[new_board == self.player] = '1'
        new_board[(new_board != '1') & (new_board != '0')] = '2'
        return str([list(k) for k in new_board])
        
        
    def update_reward(self, result):
        if result == 'W':
            result = 1
        elif result == 'L':
            result = -1
        else:
            result = 0

        self.boards.reverse()
        self.moves.reverse()
        discounted_result = result
        for i, board in enumerate(self.boards):
            state = self.q_state(board)
            q = np.array(self.expected_reward[state]).reshape(3,3)
            q[self.moves[i][0],self.moves[i][1]] = (1-self.alpha)*q[self.moves[i][0],self.moves[i][1]] + self.alpha*discounted_result
            self.expected_reward[state] = list(q.flatten())
    
        self.games_played +=1
        pickle.dump(self.expected_reward, open(self.name + '_expected_reward.p', 'wb'))
        pickle.dump(self.games_played, open(self.name + '_games_played.p', 'wb'))
    
