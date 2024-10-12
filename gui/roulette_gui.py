import tkinter as tk
from tkinter import messagebox
from game.game_logic import GameLogic
from gui.table_layout import create_roulette_table

class RouletteGUI:
    def __init__(self, master):
        self.master = master
        master.title("Roulette Game")
        self.game_logic = GameLogic()
        self.setup_gui()

    def setup_gui(self):
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_rowconfigure(2, weight=2)

        # Top frame for input fields and buttons
        top_frame = tk.Frame(self.master)
        top_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        self.create_input_fields(top_frame)

        # Frame for roulette table (centered)
        table_container = tk.Frame(self.master)
        table_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        table_container.grid_columnconfigure(0, weight=1)
        table_container.grid_columnconfigure(2, weight=1)
        
        self.table_frame = tk.Frame(table_container)
        self.table_frame.grid(row=0, column=1)
        create_roulette_table(self.table_frame, self.enter_number)

        # Frame for info text
        info_frame = tk.Frame(self.master)
        info_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        self.create_info_text(info_frame)

    def create_input_fields(self, parent):
        parent.grid_columnconfigure(1, weight=1)
        parent.grid_columnconfigure(3, weight=1)

        tk.Label(parent, text="Capital de départ:").grid(row=0, column=0, sticky="e", padx=(0, 5))
        self.capital_entry = tk.Entry(parent)
        self.capital_entry.grid(row=0, column=1, sticky="ew")

        tk.Label(parent, text="Valeur d'une pièce:").grid(row=0, column=2, sticky="e", padx=(10, 5))
        self.base_mise_entry = tk.Entry(parent)
        self.base_mise_entry.grid(row=0, column=3, sticky="ew")

        tk.Button(parent, text="Commencer", command=self.start_game).grid(row=0, column=4, padx=(10, 5))
        tk.Button(parent, text="Réinitialiser", command=self.reset_game).grid(row=0, column=5, padx=(5, 0))

    def create_info_text(self, parent):
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        self.info_text = tk.Text(parent, wrap=tk.WORD)
        self.info_text.grid(row=0, column=0, sticky="nsew")

        scrollbar = tk.Scrollbar(parent, command=self.info_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.info_text.config(yscrollcommand=scrollbar.set)

    def start_game(self):
        try:
            capital = float(self.capital_entry.get())
            base_mise = float(self.base_mise_entry.get())
            self.game_logic.initialize_game(capital, base_mise)
            self.update_info("Jeu commencé")
            self.capital_entry.config(state='disabled')
            self.base_mise_entry.config(state='disabled')
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des valeurs numériques valides.")

    def reset_game(self):
        self.game_logic.reset_game()
        self.capital_entry.config(state='normal')
        self.base_mise_entry.config(state='normal')
        self.capital_entry.delete(0, tk.END)
        self.base_mise_entry.delete(0, tk.END)
        self.info_text.delete('1.0', tk.END)
        self.update_info("Jeu réinitialisé. Veuillez entrer de nouvelles valeurs et commencer un nouveau jeu.")

    def enter_number(self, number):
        if not self.game_logic.is_initialized():
            messagebox.showwarning("Attention", "Veuillez commencer le jeu en définissant le capital et la mise de base.")
            return

        result = self.game_logic.process_number(number)
        self.update_info(result)

    def update_info(self, message):
        self.info_text.insert(tk.END, message + "\n")
        self.info_text.see(tk.END)