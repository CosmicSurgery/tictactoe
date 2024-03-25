import random
import pickle
import os
import numpy as np
import copy
from time import sleep



class tab_q:
    def __init__(self, player):
        self.name = 'tab_q'
        self.epsilon = 0.005
        self.games_played = 0
        self.max_games = 1000
        self.alpha = 0.5
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

    def update_q(self, board, moves):
        for move in moves:
            board[move[0],move[1]] = self.player
            empty_cells = [(row, col) for row in range(3) for col in range(3) if board[row][col] == 0]
            # opponent makes all possible moves, concatenate all possible states after the opponent makes a move
            for cell in empty_cells:
                board[cell[0],cell[1]] = 'H' # could be any placeholder as long as it isn't self.player or 0

            



    def get_move(self, board):
        # Generate a random move
        empty_cells = [(row, col) for row in range(3) for col in range(3) if board[row][col] == 0]
        state = self.q_state(board)
        if empty_cells:
            if state in list(self.expected_reward.keys()):
                q = self.expected_reward[state]
            else:
                q = [0.0 for k in range(len(empty_cells))]
        
            if random.uniform(0,1) < np.e**(-self.epsilon*self.games_played) and self.games_played < self.max_games:
                move =  random.choice(empty_cells)
            else:
                move = empty_cells[np.argmax(q)]
        else:
            move = None  # No valid moves available (board is full or already won)
        self.expected_reward[state] = q
        self.boards.append(copy.deepcopy(board))
        self.moves.append(move)
        return move

    def q_state(self, board):
        new_board = np.array(copy.deepcopy(board))
        new_board[new_board == self.player] = '1'
        new_board[(new_board != '1') & (new_board != '0')] = '2' # when converting to numpy, the 0's turn into strings
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
        for i, board in enumerate(self.boards):
            empty_cells = [(row, col) for row in range(3) for col in range(3) if board[row][col] == 0]
            state = self.q_state(board)
            q = np.array(self.expected_reward[state])
            if i == 0:
                q[np.where([k == self.moves[i] for k in empty_cells])[0][0]] = result
                 
            else:
                board[self.moves[i][0]][self.moves[i][1]] = self.player
                empty_cells_opp = [(row, col) for row in range(3) for col in range(3) if board[row][col] == 0]
                worst_case = []
                self.flip_player()
                for cell in empty_cells_opp:
                    board[cell[0]][cell[1]] = self.player
                    state = self.q_state(board)
                    board[cell[0]][cell[1]] = 0
                    try:
                        worst_case.append(max(self.expected_reward[state]))
                    except:
                        worst_case.append(0)
                self.flip_player()
                board[self.moves[i][0]][self.moves[i][1]] = 0
                if worst_case:
                    worst_case = -1 * max(worst_case)
                else:
                    worst_case = 0
                q[np.where([k == self.moves[i] for k in empty_cells])[0][0]] = (1-self.alpha)*q[np.where([k == self.moves[i] for k in empty_cells])[0][0]] + self.alpha*(worst_case*self.gamma)
            self.expected_reward[state] = list(q.flatten())
            # print((1-self.alpha)*q[self.moves[i][0],self.moves[i][1]] + self.alpha*discounted_result)
            # print(q[self.moves[i][0],self.moves[i][1]])

        self.games_played +=1
        pickle.dump(self.expected_reward, open(self.name + '_expected_reward.p', 'wb'))
        pickle.dump(self.games_played, open(self.name + '_games_played.p', 'wb'))
    
    def flip_player(self):
        if self.player == 'X':
            self.player = 'O'
        elif self.player == 'O':
            self.player = 'X'
        else:
            Exception('What the hell is going on here?!?!')