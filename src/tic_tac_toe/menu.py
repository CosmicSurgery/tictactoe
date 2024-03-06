import tkinter as tk
from tkinter import ttk
import subprocess
import os
import src.tic_tac_toe.bots.NaiveAI as NaiveAI

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
        # Run game.py using subprocess with additional arguments
        subprocess.run(["python", game_script, "human", "human"])


    def start_single_player(self):
        # Create a new window for single player setup
        single_player_setup_window = tk.Toplevel(self)
        single_player_setup_window.title("Single Player Setup")
        single_player_setup_window.geometry("600x300")

        # Label for X or O selection
        xo_label = tk.Label(single_player_setup_window, text="Choose X or O:", font=("Arial", 16))
        xo_label.grid(row=0, column=0, padx=10, pady=10)

        # Dropdown for X or O selection
        xo_var = tk.StringVar()
        xo_dropdown = ttk.Combobox(single_player_setup_window, textvariable=xo_var, values=["X", "O"], state="readonly", font=("Arial", 14))
        xo_dropdown.current(0)
        xo_dropdown.grid(row=0, column=1, padx=10, pady=10)

        # Label for AI type selection
        ai_label = tk.Label(single_player_setup_window, text="Choose AI Type:", font=("Arial", 16))
        ai_label.grid(row=1, column=0, padx=10, pady=10)

        from src.tic_tac_toe.bots.NaiveAI import NaiveAI
        from src.tic_tac_toe.bots.milesbot import milesbot

        ai_class_mapping = {
            "NaiveAI": NaiveAI,
            "milesbot": milesbot
        }

        # Dropdown for AI type selection
        ai_var = tk.StringVar()
        ai_dropdown = ttk.Combobox(single_player_setup_window, textvariable=ai_var, values=list(ai_class_mapping.keys()), state="readonly", font=("Arial", 14))
        ai_dropdown.current(0)
        ai_dropdown.grid(row=1, column=1, padx=10, pady=10)

        def start_game():
            xo_choice = xo_var.get()
            ai_choice = ai_var.get()

            # Get the directory path of the current script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            # Construct the full path to game.py
            game_script = os.path.join(script_dir, "game.py")
            # Run game.py using subprocess with additional arguments
            # Determine the player types based on the user's choices
            x_status = "human" if xo_choice == "X" else "ai"
            o_status = "ai" if x_status == "human" else "human"

            # Run game.py using subprocess with additional arguments
            subprocess.run(["python", game_script, x_status, o_status, ai_choice])
            single_player_setup_window.destroy()

        # Button to start the game
        play_button = tk.Button(single_player_setup_window, text="Play", command=start_game, width=20, height=3, font=("Arial", 16))
        play_button.grid(row=2, columnspan=2, pady=20)

    def start_ai(self):
        # Create a new window for single player setup
        ai_setup_window = tk.Toplevel(self)
        ai_setup_window.title("AI Sim Setup")
        ai_setup_window.geometry("600x300")

        from src.tic_tac_toe.bots.NaiveAI import NaiveAI, milesbot

        ai_class_mapping = {
            "NaiveAI": NaiveAI,
            "milesbot": milesbot
        }

        # Label for AI type selection
        ai_label_1 = tk.Label(ai_setup_window, text="X: Choose AI Type:", font=("Arial", 16))
        ai_label_1.grid(row=0, column=0, padx=10, pady=10)

        # Dropdown for AI type selection
        ai_var_1 = tk.StringVar()
        ai_dropdown_1 = ttk.Combobox(ai_setup_window, textvariable=ai_var_1, values=list(ai_class_mapping.keys()), state="readonly", font=("Arial", 14))
        ai_dropdown_1.current(0)
        ai_dropdown_1.grid(row=0, column=1, padx=10, pady=10)

        # Dropdown for AI type selection
        ai_var_2 = tk.StringVar()
        ai_dropdown_2 = ttk.Combobox(ai_setup_window, textvariable=ai_var_2, values=list(ai_class_mapping.keys()), state="readonly", font=("Arial", 14))
        ai_dropdown_2.current(1)
        ai_dropdown_2.grid(row=1, column=1, padx=10, pady=10)

        # Label for AI type selection
        ai_label_2 = tk.Label(ai_setup_window, text="O: Choose AI Type:", font=("Arial", 16))
        ai_label_2.grid(row=1, column=0, padx=10, pady=10)

        def start_sim():
            ai_model_1 = ai_var_1.get()
            ai_model_2 = ai_var_2.get()

            # Get the directory path of the current script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            # Construct the full path to game.py
            game_script = os.path.join(script_dir, "game.py")
            # Run game.py using subprocess with additional arguments
            # Determine the player types based on the user's choices
            x_status = "ai"
            o_status = "ai"

            # Run game.py using subprocess with additional arguments
            subprocess.run(["python", game_script, x_status, o_status, ai_model_1, ai_model_2, '20'])
            ai_setup_window.destroy()

        # Button to start the game
        play_button = tk.Button(ai_setup_window, text="Start sim", command=start_sim, width=20, height=3, font=("Arial", 16))
        play_button.grid(row=2, columnspan=2, pady=20)

    def start_stats(self):
        pass

if __name__ == "__main__":
    app = TicTacToeMenu()
    app.mainloop()
