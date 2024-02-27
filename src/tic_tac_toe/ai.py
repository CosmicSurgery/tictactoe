import random

class NaiveAI:
    def __init__(self):
        self.name = 'NaiveAI'

    def get_move(self, board):
        # Generate a random move
        empty_cells = [(row, col) for row in range(3) for col in range(3) if board[row][col] == 0]
        if empty_cells:
            return random.choice(empty_cells)
        else:
            return None  # No valid moves available (board is full or already won)

class milesbot:
    def __init__(self):
        self.name = 'milesbot'

    def get_move(self, board):
        # Generate a random move
        empty_cells = [(row, col) for row in range(3) for col in range(3) if board[row][col] == 0]
        if empty_cells:
            return random.choice(empty_cells)
        else:
            return None  # No valid moves available (board is full or already won)
