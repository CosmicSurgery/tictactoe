import tkinter as tk
from tkinter import messagebox
import sys
import sqlite3

class TicTacToe:
    def __init__(self, x_status, o_status): # x_status/o_status are either 'human' or 'ai'
        self.board = [[0 for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'  # Start with 'X'
        self.player_status = {'X': x_status, 'O': o_status}

    def make_move(self, row, col):
        if self.board[row][col] == 0:
            self.board[row][col] = self.current_player
            return True
        else:
            return False

    def check_win(self):
        lines = self.board + list(zip(*self.board)) + [(self.board[0][0], self.board[1][1], self.board[2][2]), (self.board[0][2], self.board[1][1], self.board[2][0])]
        return any(all(cell == line[0] and cell != 0 for cell in line) for line in lines)

    def check_draw(self):
        return all(cell != 0 for row in self.board for cell in row)
    
    def reset_board(self):
        for i in range(3):
            for j in range(3):
                self.board[i][j] = 0

class TicTacToeGUI:
    def __init__(self, master, x_status, o_status, ai_class):
        self.master = master
        self.master.title("Tic Tac Toe")
        self.game = TicTacToe(x_status, o_status)
        self.create_board_buttons()
        self.current_player_label = tk.Label(master, text=f"Current Player: {self.game.current_player}", font=("Arial", 12))
        self.current_player_label.grid(row=3, column=0, columnspan=3)
        if self.game.player_status['O'] == 'ai':
            self.ai_model = ai_class('O')
        elif self.game.player_status['X'] == 'ai':
            self.ai_model = ai_class('X')
            (row, col) = self.ai_model.get_move(self.game.board)
            self.move_validation(row,col,'ai')
        else:
            self.ai_model = None


    def create_board_buttons(self):
        self.buttons = []
        for i in range(3):
            row_buttons = []
            for j in range(3):
                button = tk.Button(self.master, text=" ", font=("Arial", 20), width=4, height=2,
                                   command=lambda row=i, col=j: self.move_validation(row, col, 'human'))
                button.grid(row=i, column=j, padx=5, pady=5)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

    def move_validation(self, row, col, status):
        if self.game.player_status[self.game.current_player] == status:
            self.handle_click(row, col)

    def handle_click(self, row, col):        
        # Get the status of the current player
        if self.game.make_move(row, col):
            player_symbol = self.game.current_player
            self.buttons[row][col].config(text=player_symbol)
            self.game.current_player = 'O' if self.game.current_player == 'X' else 'X'
            if self.game.check_win():
                messagebox.showinfo("Game Over", f"Player {player_symbol} wins!")
                self.reset_board()
            elif self.game.check_draw():
                messagebox.showinfo("Game Over", "It's a tie!")
                self.reset_board()
            else:
                self.current_player_label.config(text=f"Current Player: {player_symbol}")
                if self.ai_model is not None:
                    (row, col) = self.ai_model.get_move(self.game.board)
                    self.move_validation(row,col,'ai')
            

    def reset_board(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=" ")
                self.game.board[i][j] = 0
        self.game.current_player = 'X'
        self.current_player_label.config(text=f"Current Player: {self.game.current_player}")

def main(x_status, o_status, ai_class_name=None):
    ai_model = None
    if ai_class_name is not None:
        # Import the AI class dynamically
        ai_class = getattr(__import__('ai'), ai_class_name)
        # Instantiate the AI class
    root = tk.Tk()
    gui = TicTacToeGUI(root, x_status, o_status, ai_class_name)
    root.mainloop()

def ai_sim(ai_class_1, ai_class_2, round_lim):
    ai_class_1, ai_class_2 = getattr(__import__('ai'), ai_class_1), getattr(__import__('ai'), ai_class_2)
    ai_model_1, ai_model_2 = ai_class_1('X'), ai_class_2('O')
    ai_model_1_wins=0
    ai_model_2_wins=0
    draws = 0

    round_lim = int(round_lim)
    game = TicTacToe('ai','ai')

    round = 0
    
    while(round < round_lim):
        turn=0
        while(True):
            game.current_player = 'X'
            move = ai_model_1.get_move(game.board)
            if(move is not None):
                game.make_move(*move)
                turn+=1
            else:
                print('BAD MOVE')
            if game.check_win():
                record_result(ai_model_1, ai_model_2, ['W','L'], turn)
                ai_model_1_wins+=1
                break
            elif game.check_draw():
                record_result(ai_model_1, ai_model_2, ['D','D'], turn)
                draws+=1
                break

            game.current_player = 'O'
            move = ai_model_2.get_move(game.board)
            if(move is not None):
                game.make_move(*move)
                turn+=1
            else:
                print('BAD MOVE')
            if game.check_win():
                record_result(ai_model_1, ai_model_2, ['L','W'], turn)
                ai_model_2_wins+=1
                break
            elif game.check_draw():
                record_result(ai_model_1, ai_model_2, ['D','D'], turn)
                draws+=1
                break
        print(game.board)
        game.reset_board()
        print(round)
        round+=1
    messagebox.showinfo("Simulation Completed!", f"Final Score:{ai_model_1_wins} - {draws} - {ai_model_2_wins}")

def record_result(ai_model_1, ai_model_2, result, turns): # need to add in if they were 'X' or 'O'
    db_path_1 = f"results/{ai_model_1.name}.db"
    db_path_2 = f"results/{ai_model_2.name}.db"

    # Connect to the database for AI model 1 or create if it doesn't exist
    conn_1, conn_2 = sqlite3.connect(db_path_1), sqlite3.connect(db_path_2)
    c_1, c_2 = conn_1.cursor(), conn_2.cursor()

    # Create table if it doesn't exist
    c_1.execute('''CREATE TABLE IF NOT EXISTS results (result STRING, type STRING, turns INTEGER)''')
    c_2.execute('''CREATE TABLE IF NOT EXISTS results (result STRING, type STRING, turns INTEGER)''')

    # Insert game result into the database for AI model 1
    c_1.execute('''INSERT INTO results (result, type, turns) VALUES (?, ?, ?)''', (result[0], 'X', turns))  # Assuming AI model 1 won
    c_2.execute('''INSERT INTO results (result, type, turns) VALUES (?, ?, ?)''', (result[1], 'X', turns))  # Assuming AI model 1 won

    # Commit changes and close connection
    conn_1.commit()
    conn_1.close()    # Commit changes and close connection
    conn_2.commit()
    conn_2.close()



if __name__ == "__main__":
    if len(sys.argv) >= 5: # this means ai vs ai!
        ai_sim(sys.argv[3], sys.argv[4], sys.argv[5])
    elif len(sys.argv) >= 4:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'human' and sys.argv[2] == 'human' and len(sys.argv) >=3:
        main(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python game.py [x_status] [o_status] [ai_class_name]")
