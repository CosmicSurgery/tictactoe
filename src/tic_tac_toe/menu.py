import tkinter as tk
import subprocess
import os

class TicTacToeMenu(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Menu")
        self.geometry("400x500")

        label = tk.Label(self, text="Tic Tac Toe", font=("Arial", 18))
        label.pack()

        single_player_button = tk.Button(self, text="Single Player", command=self.start_single_player, width=20, height=3, font=("Arial", 14))
        single_player_button.pack()

        multiplayer_button = tk.Button(self, text="Multiplayer", command=self.start_multiplayer, width=20, height=3, font=("Arial", 14))
        multiplayer_button.pack()

        ai_button = tk.Button(self, text="AI", command=self.start_ai, width=20, height=3, font=("Arial", 14))
        ai_button.pack()

        stats_button = tk.Button(self, text="Stats", command=self.start_stats, width=20, height=3, font=("Arial", 14))
        stats_button.pack()

        # Bind the destroy event to close_window method
        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def close_window(self):
        # Close the window
        self.destroy()

    def start_multiplayer(self):
        # Get the directory path of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the full path to game.py
        game_script = os.path.join(script_dir, "game.py")
        # Run game.py using subprocess
        subprocess.run(["python", game_script])

    def start_single_player(self):
        pass

    def start_ai(self):
        pass

    def start_stats(self):
        pass

if __name__ == "__main__":
    app = TicTacToeMenu()
    app.mainloop()
