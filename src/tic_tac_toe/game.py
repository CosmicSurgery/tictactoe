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
    def __init__(self, master, x_status, o_status, ai_model):
        self.master = master
        self.master.title("Tic Tac Toe")
        self.game = TicTacToe(x_status, o_status)
        self.create_board_buttons()
        self.current_player_label = tk.Label(master, text=f"Current Player: {self.game.current_player}", font=("Arial", 12))
        self.current_player_label.grid(row=3, column=0, columnspan=3)
        self.ai_model = ai_model
        if self.game.player_status['X'] == 'ai':
            (row, col) = self.ai_model.get_move(self.game.board)
            self.move_validation(row,col,'ai')

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
        ai_model = ai_class()
    root = tk.Tk()
    gui = TicTacToeGUI(root, x_status, o_status, ai_model)
    root.mainloop()

def ai_sim(ai_model_1, ai_model_2, round_lim):
    ai_model_1, ai_model_2 = getattr(__import__('ai'), ai_model_1), getattr(__import__('ai'), ai_model_2)
    round_lim = int(round_lim)
    game = TicTacToe('ai','ai')

    round = 0
    
    while(round < round_lim):
        turn=0
        while(True):
            move = ai_model_1.get_move(ai_model_1, game.board)
            if(move is not None):
                game.make_move(*move)
                turn+=1
            if game.check_win():
                break
            elif game.check_draw():
                break
            move = ai_model_2.get_move(ai_model_2, game.board)
            if(move is not None):
                game.make_move(*move)
                turn+=1
            if game.check_win():
                break
            elif game.check_draw():
                break
        print(round,end='\r')
        round+=1
    messagebox.showinfo("Simulation Completed!", f"Final Score:")

def record_result(winner, loser, turns):
    # Connect to the database for AI model 1 or create if it doesn't exist
    db_name_1 = f"{winner.name}.db"
    conn_1 = sqlite3.connect(db_name_1)
    c_1 = conn_1.cursor()

    # Create table if it doesn't exist
    c_1.execute('''CREATE TABLE IF NOT EXISTS results (wins INTEGER, turns INTEGER)''')

    # Insert game result into the database for AI model 1
    c_1.execute('''INSERT INTO results (wins, turns) VALUES (?, ?)''', (1, turns))  # Assuming AI model 1 won

    # Commit changes and close connection
    conn_1.commit()
    conn_1.close()

    # Connect to the database for AI model 2 or create if it doesn't exist
    db_name_2 = f"{loser.name}.db"
    conn_2 = sqlite3.connect(db_name_2)
    c_2 = conn_2.cursor()

    # Create table if it doesn't exist
    c_2.execute('''CREATE TABLE IF NOT EXISTS results (wins INTEGER, turns INTEGER)''')

    # Insert game result into the database for AI model 2
    c_2.execute('''INSERT INTO results (wins, turns) VALUES (?, ?)''', (0, turns))  # Assuming AI model 2 lost

    # Commit changes and close connection
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
