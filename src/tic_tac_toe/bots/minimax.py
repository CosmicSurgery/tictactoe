import random
import pickle
import os
import numpy as np
import copy



class minimax:
    def __init__(self, player):
        self.name = 'minimax'
        self.player = player
        if self.player == 'X':
            self.other_player = 'O'
        else:
            self.other_player = 'X'

    def get_move(self, board, player=None):
        return self.get_move_wrapper(board,player=player)[1]

    def get_move_wrapper(self, board, player=None): # this needs to be a recursive definition right?
        empty_cells = [(row, col) for row in range(3) for col in range(3) if board[row][col] == 0]
        if empty_cells:
            cell_values = np.zeros(len(empty_cells))
            for i,(row,col) in enumerate(empty_cells):
                new_board = copy.deepcopy(board)
                new_board[row][col] = player if player is not None else self.player
                if self.check_win(new_board):
                    if player == None:
                        return 1 - len(empty_cells)/10, (row,col)
                    else:
                        return -(1 - len(empty_cells)/10), (row,col)
                if player == None:
                    cell_values[i], (_,_) = self.get_move_wrapper(new_board, player=self.other_player)
                else:
                    cell_values[i], (_,_) = self.get_move_wrapper(new_board)
            if player == None:
                return max(cell_values), empty_cells[np.argmax(cell_values)]
            else:
                return min(cell_values), empty_cells[np.argmax(cell_values)]
        else:
            return 0, (None,None)
        
    def check_win(self, board):
        lines = board + list(zip(*board)) + [(board[0][0], board[1][1], board[2][2]), (board[0][2], board[1][1], board[2][0])]
        return any(all(cell == line[0] and cell != 0 for cell in line) for line in lines)

    def update_reward(self, player):
        pass
