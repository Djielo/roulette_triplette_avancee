from game.sixain_game import SixainGame
from utils.calculations import get_sixain, get_douzaine, get_colonne, calculate_gain, arrondir

class GameLogic:
    def __init__(self):
        self.capital = 0
        self.initial_capital = 0
        self.base_mise = 0
        self.history = []
        self.active_game = None
        self.previous_capital = 0  # Capital après la sortie précédente
        self.initialized = False

    def initialize_game(self, capital, base_mise):
        self.capital = capital
        self.initial_capital = capital
        self.base_mise = base_mise
        self.history = []
        self.active_game = None
        self.previous_capital = 0
        self.initialized = True

    def reset_game(self):
        self.__init__()

    def is_initialized(self):
        return self.initialized

    def process_number(self, number):
        if not self.initialized:
            return "Le jeu n'a pas encore été initialisé."

        self.history.append(number)
        sixain = get_sixain(number)
        douzaine = get_douzaine(number)
        colonne = get_colonne(number)
        
        info = f"Numéro sorti : {number} | Sixain : S{sixain} | Douzaine : D{douzaine} | Colonne : C{colonne}\n"
        
        if len(self.history) < 10:
            return info + f"Attente de {10 - len(self.history)} numéro(s) supplémentaire(s) avant de commencer à jouer."
        
        if self.active_game:
            result_info = self.process_result(number)
            info += result_info
        
        if self.active_game is None:
            missing_sixain = self.detect_missing_sixain()
            if missing_sixain:
                self.active_game = SixainGame(missing_sixain, self.base_mise)
                self.previous_capital = self.capital  # Initialisation du capital précédent
                info += f"Nouveau sixain à jouer : S{missing_sixain}\n"
        
        if self.active_game:
            bet_info = self.place_bets()
            info += bet_info
        
        return info

    def detect_missing_sixain(self):
        last_10_sixains = [get_sixain(n) for n in self.history[-10:]]
        for sixain in range(1, 7):
            if sixain not in last_10_sixains:
                return sixain
        return None

    def process_result(self, number):
        if not self.active_game:
            return "Aucun jeu actif.\n"
        
        sixain_win = self.active_game.sixain == get_sixain(number)
        douzaine_win = self.active_game.douzaine == get_douzaine(number)
        colonne_win = self.active_game.colonne == get_colonne(number)
        
        gain_sixain = calculate_gain(sixain_win, False, False, self.active_game.last_bet)
        gain_douzaine = calculate_gain(False, douzaine_win, False, self.active_game.last_bet)
        gain_colonne = calculate_gain(False, False, colonne_win, self.active_game.last_bet)
        
        total_gain = gain_sixain + gain_douzaine + gain_colonne
        new_capital = self.capital + total_gain
        
        info = f"Gains : S: {arrondir(gain_sixain)}€, D: {arrondir(gain_douzaine)}€, C: {arrondir(gain_colonne)}€\n" \
               f"Gain total : {arrondir(total_gain)}€\n" \
               f"Nouveau capital : {arrondir(new_capital)}€\n"
        
        if new_capital < self.previous_capital:
            self.active_game.next_coup()
            info += f"Nouveau capital inférieur. Passage au coup {self.active_game.current_coup}.\n"
        elif new_capital == self.previous_capital:
            info += f"Nouveau capital égal. On reste au coup {self.active_game.current_coup}.\n"
        elif new_capital > self.previous_capital and new_capital < self.initial_capital:
            if self.active_game.current_coup > 1:
                self.active_game.previous_coup()
                info += f"Nouveau capital supérieur mais inférieur au capital de départ. Retour au coup {self.active_game.current_coup}.\n"
            else:
                info += f"Déjà au premier coup. On reste au coup {self.active_game.current_coup}.\n"
        else:  # new_capital > self.previous_capital and new_capital >= self.initial_capital
            self.active_game = None
            info += "Bénéfice réalisé. Fin du jeu sur ce sixain.\n"
        
        self.capital = new_capital
        self.previous_capital = new_capital
        
        return info

    def place_bets(self):
        if self.active_game is None:
            missing_sixain = self.detect_missing_sixain()
            if missing_sixain:
                self.active_game = SixainGame(missing_sixain, self.base_mise)
                return f"Nouveau sixain à jouer : S{missing_sixain}\n"
            else:
                return "Aucun sixain orphelin détecté. En attente...\n"

        bet = self.active_game.calculate_bet()
        total_mise = bet * 3  # Mise sur sixain, douzaine et colonne
        
        if total_mise > self.capital:
            self.active_game = None
            return "Capital insuffisant pour placer la mise. Fin du jeu sur ce sixain."
        
        self.capital -= total_mise
        self.active_game.update_mises(total_mise)
        
        return f"Mise placée : {arrondir(total_mise)}€ sur S{self.active_game.sixain}, D{self.active_game.douzaine}, C{self.active_game.colonne}\n" \
               f"Capital après mise : {arrondir(self.capital)}€\n" \
               f"Coup actuel : {self.active_game.current_coup} (Multiplicateur : x{self.active_game.bet_progression[self.active_game.current_coup - 1]})\n"