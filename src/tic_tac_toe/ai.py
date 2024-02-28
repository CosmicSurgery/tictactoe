import random
import pickle
import os
import numpy as np

class NaiveAI:
    def __init__(self, player):
        self.name = 'NaiveAI'
        self.expected_reward = {}
        self.moves = []
        self.player = player

    def get_move(self, board):
        # Generate a random move
        empty_cells = [(row, col) for row in range(3) for col in range(3) if board[row][col] == 0]
        if empty_cells:
            return random.choice(empty_cells)
        else:
            return None  # No valid moves available (board is full or already won)
    
    def update_reward(self):
        pass

class milesbot:
    def __init__(self, player):
        self.name = 'milesbot'
        self.GAMMA = 100
        self.expected_reward = {}
        self.player = player
        try:
            self.expected_reward = pickle.load(open(self.name + '_expected_reward','wb'))
        except:
            self.expected_reward = {}

    def get_move(self, board):
        # Generate a random move

        empty_cells = [(row, col) for row in range(3) for col in range(3) if board[row][col] == 0]

        
        if empty_cells:
            cell_values = np.zeros(len(empty_cells))
            for i,cell in enumerate(empty_cells):
                for state in self.get_state(*cell, board):
                    try:
                        cell_values[i] += self.expected_reward[str(state)]
                    except:
                        self.expected_reward[str(state)] = 0
            
            move = empty_cells[np.argmax(cell_values)]
        else:
            move = None  # No valid moves available (board is full or already won)
        
        return move
        
    def update_reward(self, result):
        for i, key in enumerate(self.moves):
            self.expected_reward[key] += (result/i)
        
        pickle.dump(self.expected_reward, open(self.name + '_expected_reward', 'wb'))
    
    def get_state(self, row, col, board):
        # Get row
        row_values = [1 if cell == self.player else 2 if cell != self.player != 0 else cell for cell in board[row]]

        # Get column
        col_values = [1 if board[i][col] == self.player else 2 if board[i][col] != self.player != 0 else board[i][col] for i in range(3)]

        # Get diagonal if the square is part of it
        diagonal_values = []
        if row == col or row + col == 2:
            diagonal_values = [1 if board[i][i] == self.player else 2 if board[i][i] != self.player != 0 else board[i][i] for i in range(3)]

        # Also get the anti-diagonal if the square is in the center
        anti_diagonal_values = []
        if row == col == 1:
            anti_diagonal_values = [1 if board[i][2-i] == self.player else 2 if board[i][2-i] != self.player != 0 else board[i][2-i] for i in range(3)]
            return [row_values, col_values, diagonal_values, anti_diagonal_values]
        else:
            return [row_values, col_values, diagonal_values]
