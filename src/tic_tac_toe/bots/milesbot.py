import random
import pickle
import os
import numpy as np
import copy



class milesbot:
    def __init__(self, player):
        self.name = 'milesbot'
        self.GAMMA = 100
        self.alpha = 0.1
        self.games_played = 0
        self.expected_reward = {}
        self.player = player
        self.states = []
        self.moves = []
        self.boards = []
        try:
            self.expected_reward = pickle.load(open(self.name + '_expected_reward.p','rb')) # expected_reward = pickle.load(open('milesbot_expected_reward.p','rb'))
        except:
            print('cant find')

    def get_move(self, board):
        # Generate a random move
        empty_cells = [(row, col) for row in range(3) for col in range(3) if board[row][col] == 0]

        
        if empty_cells:
            cell_values = np.zeros(len(empty_cells))
            for i,cell in enumerate(empty_cells):
                for j, state in enumerate(self.get_state(*cell, board)):
                    try:
                        if j == 1:
                            cell_values[i] += self.expected_reward[str(state)][cell[0]]
                        else:
                            cell_values[i] += self.expected_reward[str(state)][cell[1]]
                    except:
                        self.expected_reward[str(state)] = [0,0,0]
            
            move = empty_cells[np.argmax(cell_values)]
        else:
            move = None  # No valid moves available (board is full or already won)

        self.boards.append(copy.deepcopy(board))
        self.moves.append(move)

        return move
        
    def update_reward(self, result):
        if result == 'W':
            result = 1
        elif result == 'L':
            result = -1
        else:
            result = 0
        self.moves.reverse()
        self.boards.reverse()
        for i, move in enumerate(self.moves):
            true_alpha = (self.alpha/(i+1))
            vec = self.get_state(*move, self.boards[i])
            # print(self.expected_reward[str(vec[2])])
            self.expected_reward[str(vec[0])][move[1]] = (1-true_alpha)*self.expected_reward[str(vec[0])][move[1]] + true_alpha*result
            self.expected_reward[str(vec[1])][move[0]] = (1-true_alpha)*self.expected_reward[str(vec[1])][move[0]] + true_alpha*result
            if len(vec)==2:
                # then I know it's just a row and a column
                pass
            elif len(vec)==3:
                # then I know it's a corner
                self.expected_reward[str(vec[2])][move[1]] = (1-true_alpha)*self.expected_reward[str(vec[2])][move[1]] + true_alpha*result
            else:
                self.expected_reward[str(vec[2])][move[1]] = (1-true_alpha)*self.expected_reward[str(vec[2])][move[1]] + true_alpha*result
                self.expected_reward[str(vec[3])][move[1]] = (1-true_alpha)*self.expected_reward[str(vec[3])][move[1]] + true_alpha*result
        
        pickle.dump(self.expected_reward, open(self.name + '_expected_reward.p', 'wb'))
    
    def get_state(self, row, col, board):
        # Get row
        row_values = [1 if cell == self.player else 2 if cell != 0 else cell for cell in board[row]]

        # Get column
        col_values = [1 if board[i][col] == self.player else 2 if board[i][col] != 0 else board[i][col] for i in range(3)]

        # Get diagonal if the square is part of it
        diagonal_values = []
        if row == col:
            diagonal_values = [1 if board[i][i] == self.player else 2 if board[i][i] != 0 else board[i][i] for i in range(3)]

        # Also get the anti-diagonal if the square is in the center
        anti_diagonal_values = []
        if row + col == 2:
            anti_diagonal_values = [1 if board[2-i][i] == self.player else 2 if board[2-i][i] != 0 else board[2-i][i] for i in range(3)]


        if diagonal_values != [] and anti_diagonal_values != []:
            return row_values, col_values, diagonal_values, anti_diagonal_values
        elif diagonal_values == [] and anti_diagonal_values == []:
            return row_values, col_values
        elif diagonal_values != []:
            return row_values, col_values, diagonal_values
        elif anti_diagonal_values != []:
            return row_values, col_values, anti_diagonal_values

