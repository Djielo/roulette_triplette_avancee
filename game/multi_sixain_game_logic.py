from game.sixain_game import SixainGame
from utils.calculations import get_sixain, get_douzaine, get_colonne, calculate_gain, arrondir

class MultiSixainGameLogic:
    def __init__(self):
        self.capital = 0
        self.initial_capital = 0
        self.base_mise = 0
        self.history = []
        self.active_games = {}  # Un dictionnaire pour stocker les jeux actifs pour chaque sixain
        self.previous_capitals = {}  # Capital après la sortie précédente pour chaque sixain
        self.initialized = False

    def initialize_game(self, capital, base_mise):
        self.capital = capital
        self.initial_capital = capital
        self.base_mise = base_mise
        self.history = []
        self.active_games = {}
        self.previous_capitals = {i: capital for i in range(1, 7)}  # Initialisation pour chaque sixain
        self.initialized = True

    def reset_game(self):
        self.__init__()

    def is_initialized(self):
        return self.initialized

    def process_number(self, number):
        if not self.initialized:
            return "Le jeu n'a pas encore été initialisé."

        self.history.append(number)
        current_sixain = get_sixain(number)
        douzaine = get_douzaine(number)
        colonne = get_colonne(number)
        
        info = f"Numéro sorti : {number} | Sixain : S{current_sixain} | Douzaine : D{douzaine} | Colonne : C{colonne}\n"
        
        if len(self.history) < 10:
            return info + f"Attente de {10 - len(self.history)} numéro(s) supplémentaire(s) avant de commencer à jouer."
        
        for sixain in range(1, 7):
            if sixain in self.active_games:
                result_info = self.process_result(number, sixain)
                info += result_info
            
            if sixain not in self.active_games and self.should_start_game(sixain):
                self.active_games[sixain] = SixainGame(sixain, self.base_mise)
                self.previous_capitals[sixain] = self.capital
                info += f"Nouveau jeu démarré pour le sixain S{sixain}\n"
            
            if sixain in self.active_games:
                bet_info = self.place_bets(sixain)
                info += bet_info
        
        return info

    def should_start_game(self, sixain):
        last_10_sixains = [get_sixain(n) for n in self.history[-10:]]
        return sixain not in last_10_sixains

    def process_result(self, number, sixain):
        game = self.active_games[sixain]
        current_sixain = get_sixain(number)
        
        sixain_win = game.sixain == current_sixain
        douzaine_win = game.douzaine == get_douzaine(number)
        colonne_win = game.colonne == get_colonne(number)
        
        gain_sixain = calculate_gain(sixain_win, False, False, game.last_bet)
        gain_douzaine = calculate_gain(False, douzaine_win, False, game.last_bet)
        gain_colonne = calculate_gain(False, False, colonne_win, game.last_bet)
        
        total_gain = gain_sixain + gain_douzaine + gain_colonne
        new_capital = self.capital + total_gain
        
        info = f"Sixain S{sixain} - Gains : S: {arrondir(gain_sixain)}€, D: {arrondir(gain_douzaine)}€, C: {arrondir(gain_colonne)}€\n" \
               f"Gain total : {arrondir(total_gain)}€\n" \
               f"Nouveau capital : {arrondir(new_capital)}€\n"
        
        if new_capital < self.previous_capitals[sixain]:
            game.next_coup()
            info += f"Capital inférieur pour S{sixain}. Passage au coup {game.current_coup}.\n"
        elif new_capital == self.previous_capitals[sixain]:
            info += f"Capital égal pour S{sixain}. On reste au coup {game.current_coup}.\n"
        elif new_capital > self.previous_capitals[sixain] and new_capital < self.initial_capital:
            if game.current_coup > 1:
                game.previous_coup()
                info += f"Capital supérieur mais inférieur au capital de départ pour S{sixain}. Retour au coup {game.current_coup}.\n"
            else:
                info += f"Déjà au premier coup pour S{sixain}. On reste au coup {game.current_coup}.\n"
        else:  # new_capital > self.previous_capitals[sixain] and new_capital >= self.initial_capital
            del self.active_games[sixain]
            info += f"Bénéfice réalisé pour S{sixain}. Fin du jeu sur ce sixain.\n"
        
        self.capital = new_capital
        self.previous_capitals[sixain] = new_capital
        
        return info

    def place_bets(self, sixain):
        game = self.active_games[sixain]
        bet = game.calculate_bet()
        total_mise = bet * 3  # Mise sur sixain, douzaine et colonne
        
        if total_mise > self.capital:
            del self.active_games[sixain]
            return f"Capital insuffisant pour placer la mise sur S{sixain}. Fin du jeu sur ce sixain.\n"
        
        self.capital -= total_mise
        game.update_mises(total_mise)
        
        return f"S{sixain} - Mise placée : {arrondir(total_mise)}€ sur S{game.sixain}, D{game.douzaine}, C{game.colonne}\n" \
               f"Capital après mise : {arrondir(self.capital)}€\n" \
               f"Coup actuel : {game.current_coup} (Multiplicateur : x{game.bet_progression[game.current_coup - 1]})\n"