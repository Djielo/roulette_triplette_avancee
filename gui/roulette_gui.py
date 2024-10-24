import tkinter as tk
from tkinter import ttk, messagebox
from game.multi_sixain_game_logic import MultiSixainGameLogic
from gui.table_layout import create_roulette_table

class RouletteGUI:
    def __init__(self, master):
        self.master = master
        master.title("Roulette Game")
        self.game_logic = MultiSixainGameLogic()
        self.show_popup = tk.BooleanVar(value=True)
        self.coup_labels = {}  # Ajout de ce dictionnaire pour stocker les labels des coups
        self.remaining_time = 0  # Initialisation du temps restant pour le compte à rebours
        self.timer_running = False  # Statut pour savoir si le compte à rebours est actif
        self.minutes = 0  # Minutes sélectionnées
        self.seconds = 0  # Secondes sélectionnées
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

        # ====== Repositionnement du tapis de jeu à droite ======
        self.table_frame = tk.Frame(self.master)
        self.table_frame.grid(row=3, column=1, columnspan=2, padx=10, pady=10)
        create_roulette_table(self.table_frame, self.enter_number)
        # ======================================================

        # ====== Ajout du compte à rebours et des boutons de réglage ======
        timer_frame = tk.Frame(self.master)
        timer_frame.grid(row=3, column=0, columnspan=1, padx=5, pady=5)  # Le positionner à gauche

        self.timer_label = ttk.Label(timer_frame, text="00:00", font=("Arial", 16))
        self.timer_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        # Incrémenter/Décrémenter les minutes
        ttk.Button(timer_frame, text="+ Min", command=self.increment_minutes).grid(row=1, column=0, padx=2, pady=2)
        ttk.Button(timer_frame, text="- Min", command=self.decrement_minutes).grid(row=1, column=1, padx=2, pady=2)

        # Incrémenter/Décrémenter les secondes
        ttk.Button(timer_frame, text="+ Sec", command=self.increment_seconds).grid(row=2, column=0, padx=2, pady=2)
        ttk.Button(timer_frame, text="- Sec", command=self.decrement_seconds).grid(row=2, column=1, padx=2, pady=2)

        # Bouton pour démarrer le compte à rebours
        start_button = ttk.Button(timer_frame, text="Démarrer le compte à rebours", command=self.start_timer)
        start_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Bouton pour réinitialiser le compte à rebours
        reset_button = ttk.Button(timer_frame, text="Réinitialiser le compte à rebours", command=self.reset_timer)
        reset_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
        # ======================================================

    def increment_minutes(self):
        """Incrémente les minutes de 1 minute."""
        self.minutes += 1
        self.update_timer_label()

    def decrement_minutes(self):
        """Décrémente les minutes de 1 minute si possible."""
        if self.minutes > 0:
            self.minutes -= 1
        self.update_timer_label()

    def increment_seconds(self):
        """Incrémente les secondes de 10 secondes."""
        if self.seconds < 50:  # Limiter à 59 secondes
            self.seconds += 10
        else:
            self.seconds = 0
            self.increment_minutes()  # Incrémenter les minutes si les secondes dépassent 59
        self.update_timer_label()

    def decrement_seconds(self):
        """Décrémente les secondes de 10 secondes si possible."""
        if self.seconds >= 10:
            self.seconds -= 10
        elif self.minutes > 0:  # Décrémenter les minutes si les secondes passent à 0
            self.seconds = 50
            self.decrement_minutes()
        self.update_timer_label()

    def update_timer_label(self):
        """Met à jour l'affichage du label du compte à rebours."""
        self.timer_label.config(text=f"{self.minutes:02}:{self.seconds:02}")

    def start_timer(self):
        """Démarre le compte à rebours avec les minutes et secondes définies."""
        if not self.timer_running:
            self.remaining_time = self.minutes * 60 + self.seconds
            self.update_timer()
            self.timer_running = True

    def update_timer(self):
        """Met à jour le label avec le temps restant toutes les secondes."""
        if self.remaining_time > 0:
            minutes, seconds = divmod(self.remaining_time, 60)
            self.timer_label.config(text=f"{minutes:02}:{seconds:02}")
            self.remaining_time -= 1
            self.master.after(1000, self.update_timer)  # Mettre à jour toutes les secondes
        else:
            self.timer_label.config(text="00:00")
            self.timer_running = False  # Compte à rebours terminé

    def reset_timer(self):
        """Réinitialise le compte à rebours à zéro et stoppe la mise à jour."""
        self.remaining_time = 0
        self.timer_label.config(text="00:00")
        self.timer_running = False
        self.minutes = 0
        self.seconds = 0      

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

        ttk.Button(frame, text="Commencer", command=self.start_game).grid(row=3, column=1, columnspan=2, padx=5, pady=5)
        ttk.Button(frame, text="Réinitialiser", command=self.reset_game).grid(row=4, column=1, columnspan=2, padx=5, pady=5)

        ttk.Checkbutton(frame, text="Afficher les popups", variable=self.show_popup).grid(row=4, column=0, columnspan=1, padx=5, pady=5)

    def create_info_text(self, parent):
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        self.info_text = tk.Text(parent, wrap=tk.WORD)
        self.info_text.grid(row=0, column=0, sticky="nsew")

        scrollbar = tk.Scrollbar(parent, command=self.info_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.info_text.config(yscrollcommand=scrollbar.set)        

    def create_bets_gains_frame(self):
        frame = ttk.LabelFrame(self.master, text="VISUALISATION DES MISES ET GAINS")
        frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="Les mises", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(frame, text="Les gains", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=5, pady=5)

        self.bets_frame = ttk.Frame(frame)
        self.bets_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.gains_frame = ttk.Frame(frame)
        self.gains_frame.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        self.bet_labels = {}
        self.gain_labels = {}
        for i in range(6):
            self.bets_frame.columnconfigure(0, weight=1)
            self.bets_frame.columnconfigure(1, weight=1)
            self.gains_frame.columnconfigure(0, weight=1)
            self.gains_frame.columnconfigure(1, weight=1)

            ttk.Label(self.bets_frame, text=f"S{i+1} - Mises:").grid(row=i, column=0, sticky="e", padx=5, pady=2)
            self.bet_labels[i+1] = ttk.Label(self.bets_frame, text="S: 0.00€, D: 0.00€, C: 0.00€")
            self.bet_labels[i+1].grid(row=i, column=1, sticky="w", padx=5, pady=2)

            ttk.Label(self.gains_frame, text=f"S{i+1} - Gains:").grid(row=i, column=0, sticky="e", padx=5, pady=2)
            self.gain_labels[i+1] = ttk.Label(self.gains_frame, text="S: 0.00€, D: 0.00€, C: 0.00€")
            self.gain_labels[i+1].grid(row=i, column=1, sticky="w", padx=5, pady=2)

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
        frame = ttk.LabelFrame(self.master, text="VISUALISATION DU JEU")
        frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        ttk.Label(frame, text="Mises cumulées", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(frame, text="Historique des sorties", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=5, pady=5)

        # Création de la grille pour les mises cumulées        
        mises_frame = ttk.Frame(frame)
        mises_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.mises_labels = {}
        headers = ['S1:', 'S2:', 'S3:', 'S4:', 'S5:', 'S6:',
                'D1:', 'D2:', 'D3:',
                'C1:', 'C2:', 'C3:']

        # Configurer des lignes vides pour l'espacement
        mises_frame.grid_rowconfigure(2, minsize=10)  # Espace entre sixains et douzaines
        mises_frame.grid_rowconfigure(4, minsize=10)  # Espace entre douzaines et colonnes

        for i, header in enumerate(headers):
            # Calculer la position réelle en tenant compte des lignes d'espacement
            if i < 6:  # Sixains
                row = i // 3
            elif i < 9:  # Douzaines
                row = (i // 3) + 1  # +1 pour l'espace après les sixains
            else:  # Colonnes
                row = (i // 3) + 2  # +2 pour les deux espaces

            label = tk.Label(mises_frame, text=header, relief="ridge", width=4)
            label.grid(row=row, column=i%3*2, sticky="nsew", padx=1, pady=1)
            value_label = tk.Label(mises_frame, text="0.00€", relief="ridge", width=8)
            value_label.grid(row=row, column=i%3*2+1, sticky="nsew", padx=1, pady=1)
            self.mises_labels[header] = value_label

        # Ajout de la section pour les coups par sixain
        ttk.Label(frame, text="Coup par sixain", font=("Arial", 10, "bold")).grid(row=2, column=0, padx=5, pady=5)

        coups_frame = ttk.Frame(frame)
        coups_frame.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

        for i in range(6):
            label = tk.Label(coups_frame, text=f"S{i+1}:", relief="ridge", width=4)
            label.grid(row=i//3, column=i%3*2, sticky="nsew", padx=1, pady=1)
            value_label = tk.Label(coups_frame, text="-", relief="ridge", width=8)
            value_label.grid(row=i//3, column=i%3*2+1, sticky="nsew", padx=1, pady=1)
            self.coup_labels[f'S{i+1}:'] = value_label

        self.history_canvas = tk.Canvas(frame, width=200, height=200)
        self.history_canvas.grid(row=1, column=1, rowspan=3, padx=5, pady=5)

    def update_display(self):
        # Mise à jour des mises et gains
        for sixain in range(1, 7):
            if sixain in self.game_logic.active_games:
                game = self.game_logic.active_games[sixain]
                bet_text = f"S{sixain}: {game.last_bet:.2f}€, D{game.douzaine}: {game.last_bet:.2f}€, C{game.colonne}: {game.last_bet:.2f}€"
                gain_text = f"S: {game.last_gain_sixain:.2f}€, D: {game.last_gain_douzaine:.2f}€, C: {game.last_gain_colonne:.2f}€"
                
                self.bet_labels[sixain].config(text=bet_text)
                self.gain_labels[sixain].config(text=gain_text)
                self.balance_labels[sixain].config(text=f"{game.balance:.2f}€")
                
                # Mise en évidence des mises actives
                self.mises_labels[f'S{sixain}:'].config(bg='light yellow')
                self.mises_labels[f'D{game.douzaine}:'].config(bg='light yellow')
                self.mises_labels[f'C{game.colonne}:'].config(bg='light yellow')
            else:
                self.bet_labels[sixain].config(text="Inactif")
                self.gain_labels[sixain].config(text="Inactif")
                self.balance_labels[sixain].config(text="0.00€")
                self.mises_labels[f'S{sixain}:'].config(bg='SystemButtonFace')

        # Mise à jour du déroulement du jeu
        if self.game_logic.history:
            last_number = self.game_logic.history[-1]
            self.last_number.config(text=str(last_number if last_number != 37 else "00"))
        for sixain in range(1, 7):
            if sixain in self.game_logic.active_games:
                balance = self.game_logic.active_games[sixain].balance
            else:
                balance = 0
            self.balance_labels[sixain].config(text=f"{balance:.2f}€")
        self.capital_label.config(text=f"{self.game_logic.capital:.2f}€")

        # Mise à jour de la visualisation globale
        total_bets = self.calculate_total_bets()
        for category, bets in total_bets.items():
            for key, value in bets.items():
                self.mises_labels[f"{key}:"].config(text=f"{value:.2f}€")

        # Mise à jour du numéro sorti
        if self.game_logic.history:
            last_number = self.game_logic.history[-1]
            self.last_number.config(text=str(last_number if last_number != 37 else "00"))

        # Mise à jour du capital global
        self.capital_label.config(text=f"{self.game_logic.capital:.2f}€")

        # Mise à jour des mises cumulées
        total_bets = self.calculate_total_bets()
        for category in ['sixains', 'douzaines', 'colonnes']:
            for key, value in total_bets[category].items():
                self.mises_labels[f"{key}:"].config(text=f"{value:.2f}€")
                # Réinitialiser la couleur de fond
                self.mises_labels[f"{key}:"].config(bg='SystemButtonFace')

        # Mettre en évidence les mises actives
        for sixain, game in self.game_logic.active_games.items():
            self.mises_labels[f'S{sixain}:'].config(bg='light yellow')
            self.mises_labels[f'D{game.douzaine}:'].config(bg='light yellow')
            self.mises_labels[f'C{game.colonne}:'].config(bg='light yellow')

        # Mise à jour de l'historique des sorties
        self.update_history_display()

        # Mise à jour et mise en surbrillance des coups par sixain
        for sixain in range(1, 7):
            if sixain in self.game_logic.active_games:
                game = self.game_logic.active_games[sixain]
                self.coup_labels[f'S{sixain}:'].config(text=f"{game.current_coup}", bg='light yellow')
            else:
                self.coup_labels[f'S{sixain}:'].config(text="-", bg='SystemButtonFace')

    def calculate_total_bets(self):
        total_bets = {
            'sixains': {f'S{i}': 0 for i in range(1, 7)},
            'douzaines': {f'D{i}': 0 for i in range(1, 4)},
            'colonnes': {f'C{i}': 0 for i in range(1, 4)}
        }
        for sixain, game in self.game_logic.active_games.items():
            total_bets['sixains'][f'S{sixain}'] += game.last_bet
            total_bets['douzaines'][f'D{game.douzaine}'] += game.last_bet
            total_bets['colonnes'][f'C{game.colonne}'] += game.last_bet
        return total_bets

    def update_history_display(self):
        self.history_canvas.delete("all")
        for i, number in enumerate(self.game_logic.history[-30:]):  # Affiche les 30 derniers numéros
            x, y = (i % 6) * 33, (i // 6) * 33
            if number == 0 or number == 37:
                color = "green"
                text = "0" if number == 0 else "00"
            else:
                color = "red" if number in [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36] else "black"
                text = str(number)
            self.history_canvas.create_rectangle(x, y, x+30, y+30, fill=color)
            self.history_canvas.create_text(x+15, y+15, text=text, fill="white")

    def start_game(self):
        try:
            capital = float(self.capital_entry.get())
            base_mise = float(self.base_mise_entry.get())
            max_active_sixains = int(self.sixain_number.get())
            self.game_logic.initialize_game(capital, base_mise, max_active_sixains)
            self.update_display()
            if self.show_popup.get():
                messagebox.showinfo("Jeu commencé", f"Jeu commencé avec un maximum de {max_active_sixains} sixain(s) actif(s)")
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des valeurs numériques valides.")

    def reset_game(self):
        self.game_logic.reset_game()
        self.capital_entry.delete(0, tk.END)
        self.base_mise_entry.delete(0, tk.END)
        self.sixain_number.set("1")
        for sixain in range(1, 7):
            self.bet_labels[sixain].config(text="Inactif")
            self.gain_labels[sixain].config(text="Inactif")
            self.balance_labels[sixain].config(text="0.00€")
        self.last_number.config(text="--")
        self.capital_label.config(text="0.00€")
        
        # Réinitialisation des mises cumulées
        for label in self.mises_labels.values():
            label.config(text="0.00€", bg='SystemButtonFace')

        # Réinitialisation des coups par sixain
        for label in self.coup_labels.values():
            label.config(text="-", bg='SystemButtonFace')            
        
        self.history_canvas.delete("all")
        if self.show_popup.get():
            messagebox.showinfo("Jeu réinitialisé", "Le jeu a été réinitialisé.")

    def enter_number(self, number):
        if not self.game_logic.is_initialized():
            messagebox.showwarning("Attention", "Veuillez commencer le jeu en définissant le capital et la mise de base.")
            return

        result = self.game_logic.process_number(number)
        self.update_display()
        if self.show_popup.get():
            messagebox.showinfo("Résultat", result)

    def update_info(self, message):
        self.info_text.insert(tk.END, message + "\n")
        self.info_text.see(tk.END)            