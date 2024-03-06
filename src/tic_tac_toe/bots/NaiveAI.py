import random
import pickle
import os
import numpy as np
import copy

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
    
    def update_reward(self, result):
        pass

