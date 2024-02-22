import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self):
        self.board = [[0 for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'  # Start with 'X'

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

class TicTacToeGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe")
        self.game = TicTacToe()
        self.create_board_buttons()
        self.current_player_label = tk.Label(master, text=f"Current Player: {self.game.current_player}", font=("Arial", 12))
        self.current_player_label.grid(row=3, column=0, columnspan=3)

    def create_board_buttons(self):
        self.buttons = []
        for i in range(3):
            row_buttons = []
            for j in range(3):
                button = tk.Button(self.master, text=" ", font=("Arial", 20), width=4, height=2,
                                   command=lambda row=i, col=j: self.handle_click(row, col))
                button.grid(row=i, column=j, padx=5, pady=5)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

    def handle_click(self, row, col):
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

    def reset_board(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=" ")
                self.game.board[i][j] = 0
        self.game.current_player = 'X'
        self.current_player_label.config(text=f"Current Player: {self.game.current_player}")

def main():
    root = tk.Tk()
    gui = TicTacToeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
