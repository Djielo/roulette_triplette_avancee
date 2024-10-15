import tkinter as tk
from tkinter import ttk, messagebox
from game.multi_sixain_game_logic import MultiSixainGameLogic
from gui.table_layout import create_roulette_table

class RouletteGUI:
    def __init__(self, master):
        self.master = master
        master.title("Roulette Game")
        self.game_logic = MultiSixainGameLogic()
        self.setup_gui()

    def setup_gui(self):
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)

        # Paramètres de jeu
        self.create_game_params_frame()

        # Visualisation des mises et gains
        self.create_bets_gains_frame()

        # Déroulement du jeu
        self.create_game_progress_frame()

        # Visualisation globale du jeu
        self.create_global_view_frame()

        # Table de roulette (conservée de l'ancienne version)
        self.table_frame = tk.Frame(self.master)
        self.table_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        create_roulette_table(self.table_frame, self.enter_number)

    def create_game_params_frame(self):
        frame = ttk.LabelFrame(self.master, text="Paramètres de jeu")
        frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(frame, text="Capital de départ:").grid(row=0, column=0, sticky="e", padx=5, pady=2)
        self.capital_entry = ttk.Entry(frame)
        self.capital_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        ttk.Label(frame, text="Valeur d'une pièce:").grid(row=1, column=0, sticky="e", padx=5, pady=2)
        self.base_mise_entry = ttk.Entry(frame)
        self.base_mise_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=2)

        ttk.Label(frame, text="Nombre max de sixains:").grid(row=2, column=0, sticky="e", padx=5, pady=2)
        self.sixain_number = ttk.Combobox(frame, values=list(range(1, 7)))
        self.sixain_number.set("1")
        self.sixain_number.grid(row=2, column=1, sticky="ew", padx=5, pady=2)

        ttk.Button(frame, text="Commencer", command=self.start_game).grid(row=3, column=0, padx=5, pady=5)
        ttk.Button(frame, text="Réinitialiser", command=self.reset_game).grid(row=3, column=1, padx=5, pady=5)

    def create_info_text(self, parent):
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        self.info_text = tk.Text(parent, wrap=tk.WORD)
        self.info_text.grid(row=0, column=0, sticky="nsew")

        scrollbar = tk.Scrollbar(parent, command=self.info_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.info_text.config(yscrollcommand=scrollbar.set)

    def create_bets_gains_frame(self):
        frame = ttk.LabelFrame(self.master, text="Visualisation des mises et gains")
        frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.bets_text = tk.Text(frame, height=10, width=40)
        self.bets_text.grid(row=0, column=0, padx=5, pady=5)
        self.gains_text = tk.Text(frame, height=10, width=40)
        self.gains_text.grid(row=0, column=1, padx=5, pady=5)

    def create_game_progress_frame(self):
        frame = ttk.LabelFrame(self.master, text="Déroulement du jeu")
        frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(frame, text="Numéro sorti:").grid(row=0, column=0, sticky="e", padx=5, pady=2)
        self.last_number = ttk.Label(frame, text="--")
        self.last_number.grid(row=0, column=1, sticky="w", padx=5, pady=2)

        self.balance_labels = {}
        for i in range(6):
            ttk.Label(frame, text=f"Balance pour sixain {i+1}:").grid(row=i+1, column=0, sticky="e", padx=5, pady=2)
            self.balance_labels[i+1] = ttk.Label(frame, text="0.00€")
            self.balance_labels[i+1].grid(row=i+1, column=1, sticky="w", padx=5, pady=2)

        ttk.Label(frame, text="Évolution capital global:").grid(row=7, column=0, sticky="e", padx=5, pady=2)
        self.capital_label = ttk.Label(frame, text="0.00€")
        self.capital_label.grid(row=7, column=1, sticky="w", padx=5, pady=2)

    def create_global_view_frame(self):
        frame = ttk.LabelFrame(self.master, text="Visualisation globale du jeu")
        frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        self.total_bets_text = tk.Text(frame, height=10, width=40)
        self.total_bets_text.grid(row=0, column=0, padx=5, pady=5)

        self.history_canvas = tk.Canvas(frame, width=300, height=100)
        self.history_canvas.grid(row=1, column=0, padx=5, pady=5)

    def update_display(self):
        # Mise à jour des mises et gains
        self.bets_text.delete('1.0', tk.END)
        self.gains_text.delete('1.0', tk.END)
        for sixain, game in self.game_logic.active_games.items():
            self.bets_text.insert(tk.END, f"S{sixain} - Mises : S: {game.last_bet:.2f}€, D: {game.last_bet:.2f}€, C: {game.last_bet:.2f}€\n")
            self.gains_text.insert(tk.END, f"S{sixain} - Gains : S: {game.total_gain:.2f}€, D: {game.total_gain:.2f}€, C: {game.total_gain:.2f}€\n")

        # Mise à jour du déroulement du jeu
        if self.game_logic.history:
            self.last_number.config(text=str(self.game_logic.history[-1]))
        for sixain in range(1, 7):
            if sixain in self.game_logic.active_games:
                balance = self.game_logic.active_games[sixain].balance
            else:
                balance = 0
            self.balance_labels[sixain].config(text=f"{balance:.2f}€")
        self.capital_label.config(text=f"{self.game_logic.capital:.2f}€")

        # Mise à jour de la visualisation globale
        self.total_bets_text.delete('1.0', tk.END)
        total_bets = self.calculate_total_bets()
        for category, bets in total_bets.items():
            self.total_bets_text.insert(tk.END, f"{category.capitalize()}:\n")
            for key, value in bets.items():
                self.total_bets_text.insert(tk.END, f"{key}: {value:.2f}€\n")
            self.total_bets_text.insert(tk.END, "\n")

        # Mise à jour de l'historique des sorties
        self.update_history_display()

    def calculate_total_bets(self):
        total_bets = {'sixains': {}, 'douzaines': {}, 'colonnes': {}}
        for sixain, game in self.game_logic.active_games.items():
            total_bets['sixains'][f'S{sixain}'] = total_bets['sixains'].get(f'S{sixain}', 0) + game.last_bet
            total_bets['douzaines'][f'D{game.douzaine}'] = total_bets['douzaines'].get(f'D{game.douzaine}', 0) + game.last_bet
            total_bets['colonnes'][f'C{game.colonne}'] = total_bets['colonnes'].get(f'C{game.colonne}', 0) + game.last_bet
        return total_bets

    def update_history_display(self):
        self.history_canvas.delete("all")
        for i, number in enumerate(self.game_logic.history[-30:]):  # Affiche les 30 derniers numéros
            x, y = (i % 10) * 30, (i // 10) * 30
            color = "red" if number in [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36] else "black"
            self.history_canvas.create_oval(x, y, x+20, y+20, fill=color)
            self.history_canvas.create_text(x+10, y+10, text=str(number), fill="white")            

    def start_game(self):
        try:
            capital = float(self.capital_entry.get())
            base_mise = float(self.base_mise_entry.get())
            max_active_sixains = int(self.sixain_number.get())
            self.game_logic.initialize_game(capital, base_mise, max_active_sixains)
            self.update_display()
            messagebox.showinfo("Jeu commencé", f"Jeu commencé avec un maximum de {max_active_sixains} sixain(s) actif(s)")
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des valeurs numériques valides.")

    def reset_game(self):
        self.game_logic.reset_game()
        self.update_display()
        messagebox.showinfo("Jeu réinitialisé", "Le jeu a été réinitialisé.")

    def enter_number(self, number):
        if not self.game_logic.is_initialized():
            messagebox.showwarning("Attention", "Veuillez commencer le jeu en définissant le capital et la mise de base.")
            return

        result = self.game_logic.process_number(number)
        self.update_display()
        messagebox.showinfo("Résultat", result)

    def update_info(self, message):
        self.info_text.insert(tk.END, message + "\n")
        self.info_text.see(tk.END)