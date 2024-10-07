import tkinter as tk
from tkinter import messagebox, simpledialog
from typing import List, Dict, Tuple

class SixainGame:
    def __init__(self, sixain: int, base_mise: float, douzaine: int, colonne: int):
        self.sixain = sixain
        self.base_mise = base_mise
        self.douzaine = douzaine
        self.colonne = colonne
        self.coup = 1
        self.mises_globales = 0
        self.mises_totales = 0
        self.last_bet = 0

    def next_coup(self):
        if self.coup < 9:
            self.coup += 1
            print(f"Passage au coup {self.coup} pour le sixain {self.sixain}")

    def reset_coup(self):
        self.coup = 1

    def calculate_bet(self) -> float:
        bet_structure = {1: 1, 2: 1, 3: 1, 4: 2, 5: 3, 6: 5, 7: 8, 8: 15, 9: 30}
        return self.base_mise * bet_structure.get(self.coup, 30)

    def update_mises(self, mise: float):
        self.mises_globales = mise
        self.mises_totales += mise
        self.last_bet = mise

class RouletteGUI:
    def __init__(self, master):
        self.master = master
        master.title("Roulette Game")
        self.capital = 0
        self.base_mise = 0
        self.history = []
        self.games: Dict[int, SixainGame] = {}
        self.last_number = None
        self.waiting_for_result = False
        self.pending_bets = []
        self.setup_gui()

    def setup_gui(self):
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)

        # Top frame for input fields and start button
        top_frame = tk.Frame(self.master)
        top_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        top_frame.grid_columnconfigure(1, weight=1)
        top_frame.grid_columnconfigure(3, weight=1)

        tk.Label(top_frame, text="Capital de départ:").grid(row=0, column=0, sticky="e", padx=(0, 5))
        self.capital_entry = tk.Entry(top_frame)
        self.capital_entry.grid(row=0, column=1, sticky="ew")

        tk.Label(top_frame, text="Valeur d'une pièce:").grid(row=0, column=2, sticky="e", padx=(10, 5))
        self.base_mise_entry = tk.Entry(top_frame)
        self.base_mise_entry.grid(row=0, column=3, sticky="ew")

        tk.Button(top_frame, text="Commencer", command=self.start_game).grid(row=0, column=4, padx=(10, 0))

        # Main frame for roulette table and info text
        main_frame = tk.Frame(self.master)
        main_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        main_frame.grid_columnconfigure(0, weight=3)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        # Left frame for roulette table
        self.table_frame = tk.Frame(main_frame)
        self.table_frame.grid(row=0, column=0, sticky="nsew")
        self.create_roulette_table(self.table_frame)

        # Right frame for info text
        info_frame = tk.Frame(main_frame)
        info_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        info_frame.grid_rowconfigure(0, weight=1)
        info_frame.grid_columnconfigure(0, weight=1)

        self.info_text = tk.Text(info_frame, wrap=tk.WORD)
        self.info_text.grid(row=0, column=0, sticky="nsew")

        scrollbar = tk.Scrollbar(info_frame, command=self.info_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.info_text.config(yscrollcommand=scrollbar.set)

    def create_roulette_table(self, parent):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(0, weight=1)

        table = tk.Frame(parent, bg="green")
        table.grid(sticky="nsew")

        # Create number grid
        number_frame = tk.Frame(table, bg="green")
        number_frame.grid(row=0, column=1, columnspan=12, sticky="nsew", padx=3, pady=3)

        # Taille fixe pour les boutons
        btn_width = 4  # Ajuste la largeur des boutons
        btn_height = 2  # Ajuste la hauteur des boutons

        for i in range(12):
            number_frame.grid_columnconfigure(i, weight=1)
        for i in range(3):
            number_frame.grid_rowconfigure(i, weight=1)

        numbers = [
            [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36],
            [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35],
            [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]
        ]
        colors = ["red" if n in [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36] else "black" for n in range(1, 37)]

        for row, row_numbers in enumerate(numbers):
            for col, number in enumerate(row_numbers):
                color = colors[number - 1]
                btn = tk.Button(number_frame, text=str(number), bg=color, fg="white", 
                                command=lambda x=number: self.enter_number(x),
                                width=btn_width, height=btn_height)  # Applique la taille des boutons
                btn.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)

        # Create 0 and 00 button
        zero_frame = tk.Frame(table, bg="green")
        zero_frame.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        tk.Button(zero_frame, text="0", bg="green", fg="white", width=btn_width, 
                  command=lambda: self.enter_number(0)).pack(expand=True, fill="both")
        tk.Button(zero_frame, text="00", bg="green", fg="white", width=btn_width, 
                  command=lambda: self.enter_number(37)).pack(expand=True, fill="both")

        # Create bottom bets
        bottom_frame = tk.Frame(table, bg="green")
        bottom_frame.grid(row=1, column=0, columnspan=13, sticky="nsew", padx=2, pady=2)

        for i in range(6):
            bottom_frame.grid_columnconfigure(i, weight=1)
        for i in range(2):
            bottom_frame.grid_rowconfigure(i, weight=1)

        tk.Button(bottom_frame, text="D1", bg="green", fg="white", width=btn_width, height=btn_height).grid(row=0, column=0, columnspan=2, sticky="nsew", padx=1, pady=1)
        tk.Button(bottom_frame, text="D2", bg="green", fg="white", width=btn_width, height=btn_height).grid(row=0, column=2, columnspan=2, sticky="nsew", padx=1, pady=1)
        tk.Button(bottom_frame, text="D3", bg="green", fg="white", width=btn_width, height=btn_height).grid(row=0, column=4, columnspan=2, sticky="nsew", padx=1, pady=1)

        tk.Button(bottom_frame, text="1-18", bg="green", fg="white", height=btn_height).grid(row=1, column=0, sticky="nsew", padx=1, pady=1)
        tk.Button(bottom_frame, text="PAIR", bg="green", fg="white", height=btn_height).grid(row=1, column=1, sticky="nsew", padx=1, pady=1)
        tk.Button(bottom_frame, text="R", bg="red", height=btn_height).grid(row=1, column=2, sticky="nsew", padx=1, pady=1)
        tk.Button(bottom_frame, text="N", bg="black", fg="white", height=btn_height).grid(row=1, column=3, sticky="nsew", padx=1, pady=1)
        tk.Button(bottom_frame, text="IMPAIR", bg="green", fg="white", height=btn_height).grid(row=1, column=4, sticky="nsew", padx=1, pady=1)
        tk.Button(bottom_frame, text="19-36", bg="green", fg="white", height=btn_height).grid(row=1, column=5, sticky="nsew", padx=1, pady=1)

        # Create 2TO1 buttons
        twoToOne_frame = tk.Frame(table, bg="green")
        twoToOne_frame.grid(row=0, column=13, sticky="nsew", padx=2, pady=2)
        for i in range(3):
            tk.Button(twoToOne_frame, text=f"C{3-i}", bg="green", fg="white", width=btn_width, height=btn_height).grid(row=i, column=0, sticky="nsew", padx=1, pady=1)

    def start_game(self):
        try:
            self.capital = float(self.capital_entry.get())
            self.base_mise = float(self.base_mise_entry.get())
            self.reset_files()
            self.update_info(f"Jeu commencé avec un capital de {self.capital}€ et une pièce de {self.base_mise}€")
            self.capital_entry.config(state='disabled')
            self.base_mise_entry.config(state='disabled')
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des valeurs numériques valides.")

    def enter_number(self, number):
        if not self.capital:
            messagebox.showwarning("Attention", "Veuillez commencer le jeu en définissant le capital et la mise de base.")
            return

        self.history.append(number)
        self.save_history_to_file()
        
        sixain = self.get_sixain(number)
        douzaine = self.get_douzaine(number)
        colonne = self.get_colonne(number)
        
        self.update_info(f"\n0- Capital avant mises : {self.arrondir(self.capital)}€")
        self.update_info(f"Numéro sorti : {number} | Sixain : S{sixain} | Douzaine : D{douzaine} | Colonne : C{colonne}")

        if len(self.history) < 10:
            self.update_info(f"Attente de {10 - len(self.history)} numéro(s) supplémentaire(s) avant de commencer à jouer.")
            return
        
        if self.waiting_for_result:
            self.process_result(number)
            self.waiting_for_result = False
        
        missing_sixains = self.detect_missing_sixains()
        for missing_sixain in missing_sixains:
            if missing_sixain not in self.games:
                self.games[missing_sixain] = SixainGame(missing_sixain, self.base_mise, self.get_douzaine_from_sixain(missing_sixain), self.get_colonne_from_sixain(missing_sixain))
                self.update_info(f"Nouveau sixain à jouer : S{missing_sixain}")
        
        total_mise = 0
        for sixain, game in self.games.items():
            bet = game.calculate_bet()
            game_mise = bet * 3
            
            self.update_info(f"1- Coup n°{game.coup} - Mise à jouer : {self.arrondir(game_mise)} pièces sur S{sixain}, D{self.get_douzaine_from_sixain(sixain)}, C{self.get_colonne_from_sixain(sixain)}")
            
            game.update_mises(game_mise)
            total_mise += game_mise
            
            self.update_info(f"2- Mises globales pour S{sixain} = {self.arrondir(game.mises_globales)}€ | Mises totales = {self.arrondir(game.mises_totales)}€")
        
        self.capital -= total_mise
        self.update_info(f"3- Capital après mises : {self.arrondir(self.capital)}€")
        self.save_game_data()
        
        self.waiting_for_result = True

    def process_result(self, number):
        total_gain = 0
        self.update_info(f"4- Numéro sorti : {number}")
        for sixain, game in self.games.items():
            sixain_win = sixain == self.get_sixain(number)
            douzaine_win = self.get_douzaine_from_sixain(sixain) == self.get_douzaine(number)
            colonne_win = self.get_colonne_from_sixain(sixain) == self.get_colonne(number)
            
            gain_sixain = self.calculate_gain(sixain_win, False, False, game.last_bet / 3)
            gain_douzaine = self.calculate_gain(False, douzaine_win, False, game.last_bet / 3)
            gain_colonne = self.calculate_gain(False, False, colonne_win, game.last_bet / 3)
            
            self.update_info(f"5- Gains pour S{sixain}: S: {self.arrondir(gain_sixain)}€, D: {self.arrondir(gain_douzaine)}€, C: {self.arrondir(gain_colonne)}€")
            
            gain = gain_sixain + gain_douzaine + gain_colonne
            total_gain += gain
            
            capital_initial = float(self.capital_entry.get())
            if self.capital + total_gain > capital_initial:
                game.reset_coup()
            else:
                game.next_coup()

        self.capital += total_gain
        self.update_info(f"6- Gains globaux : {self.arrondir(total_gain)}€")
        self.update_info(f"0- Capital avant mises : {self.arrondir(self.capital)}€")

    def update_info(self, message):
        self.info_text.insert(tk.END, message + "\n")
        self.info_text.see(tk.END)

    @staticmethod
    def get_sixain(number: int) -> int:
        if number == 0 or number == 37:  # 37 represents 00
            return None
        return (number - 1) // 6 + 1 if 1 <= number <= 36 else None

    @staticmethod
    def get_douzaine(number: int) -> int:
        if number == 0 or number == 37:  # 37 represents 00
            return None
        return (number - 1) // 12 + 1 if 1 <= number <= 36 else None

    @staticmethod
    def get_colonne(number: int) -> int:
        if number == 0 or number == 37:  # 37 represents 00
            return None
        return (number - 1) % 3 + 1 if 1 <= number <= 36 else None

    @staticmethod
    def get_douzaine_from_sixain(sixain: int) -> int:
        return (sixain - 1) // 2 + 1 if sixain is not None and 1 <= sixain <= 6 else None

    @staticmethod
    def get_colonne_from_sixain(sixain: int) -> int:
        if sixain is None or sixain < 1 or sixain > 6:
            return None
        return [2, 1, 3, 2, 1, 3][sixain - 1]

    @staticmethod
    def calculate_gain(sixain_win: bool, douzaine_win: bool, colonne_win: bool, mise: float) -> float:
        return mise * (6 * sixain_win + 3 * douzaine_win + 3 * colonne_win)

    @staticmethod
    def arrondir(valeur: float) -> float:
        return round(valeur, 2)

    @staticmethod
    def reset_files():
        open("capital.txt", "w").close()
        open("historique.txt", "w").close()

    def save_game_data(self, filename: str = "capital.txt") -> None:
        with open(filename, "a") as file:
            file.write(f"Capital : {self.arrondir(self.capital)}€\n")
            for sixain, game in self.games.items():
                file.write(f"Sixain {sixain}: Mises globales = {self.arrondir(game.mises_globales)}€ | Mises totales = {self.arrondir(game.mises_totales)}€\n")
        print(f"Données sauvegardées dans {filename}")

    def save_history_to_file(self, filename: str = "historique.txt") -> None:
        with open(filename, "a") as file:
            file.write(", ".join(map(str, self.history)) + "\n")
        print(f"Historique sauvegardé dans {filename}")

    def detect_missing_sixains(self) -> List[int]:
        return [sixain for sixain in range(1, 7) if sixain not in [self.get_sixain(n) for n in self.history[-10:]]]

def main():
    root = tk.Tk()
    root.geometry("1000x600")  # Set initial window size
    gui = RouletteGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()