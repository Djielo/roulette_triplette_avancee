from collections import deque
from game.sixain_game import SixainGame
from utils.calculations import get_sixain, get_douzaine, get_colonne, calculate_gain, arrondir

class MultiSixainGameLogic:
    def __init__(self):
        self.capital = 0
        self.initial_capital = 0
        self.base_mise = 0
        self.history = []
        self.active_games = {}
        self.initialized = False
        self.max_active_sixains = 0
        self.orphan_sixains = []
        self.last_ten_sixains = deque(maxlen=10)

    def initialize_game(self, capital, base_mise, max_active_sixains):
        self.capital = capital
        self.initial_capital = capital
        self.base_mise = base_mise
        self.history = []
        self.active_games = {}
        self.initialized = True
        self.max_active_sixains = max_active_sixains
        self.orphan_sixains = []
        self.last_ten_sixains = deque(maxlen=10)

    def process_number(self, number):
        if not self.initialized:
            return "Le jeu n'a pas encore été initialisé."

        self.history.append(number)
        current_sixain = get_sixain(number)
        douzaine = get_douzaine(number)
        colonne = get_colonne(number)
        
        info = f"Numéro sorti : {number} | Sixain : S{current_sixain} | Douzaine : D{douzaine} | Colonne : C{colonne}\n"
        
        self.last_ten_sixains.append(current_sixain)
        
        if len(self.history) < 10:
            return info + f"Attente de {10 - len(self.history)} numéro(s) supplémentaire(s) avant de commencer à jouer."
        
        self.update_orphan_sixains(current_sixain)
        
        for sixain in list(self.active_games.keys()):
            result_info = self.process_result(number, sixain)
            info += result_info
        
        while len(self.active_games) < self.max_active_sixains and self.orphan_sixains:
            new_sixain = self.orphan_sixains.pop(0)
            self.start_new_game(new_sixain)
            info += f"Nouveau jeu démarré pour le sixain orphelin S{new_sixain}\n"
        
        for sixain in self.active_games:
            bet_info = self.place_bets(sixain)
            info += bet_info
        
        return info

    def update_orphan_sixains(self, current_sixain):
        if current_sixain in self.orphan_sixains:
            self.orphan_sixains.remove(current_sixain)
        
        for sixain in range(1, 7):
            if (sixain not in self.active_games and 
                sixain not in self.last_ten_sixains and 
                sixain not in self.orphan_sixains):
                self.orphan_sixains.append(sixain)

    def start_new_game(self, sixain):
        self.active_games[sixain] = SixainGame(sixain, self.base_mise)

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
      previous_balance = game.balance
      game.update_gains(total_gain)
      self.capital += total_gain
      
      info = f"Sixain S{sixain} - Gains : S: {arrondir(gain_sixain)}€, D: {arrondir(gain_douzaine)}€, C: {arrondir(gain_colonne)}€\n" \
            f"Gain total : {arrondir(total_gain)}€\n" \
            f"Balance du sixain : {arrondir(game.balance)}€ ({game.get_status()})\n" \
            f"Nouveau capital : {arrondir(self.capital)}€\n"
      
      if game.balance < 0:
          if game.balance > previous_balance:
              # Gain qui réduit la perte
              if game.current_coup > 1:
                  game.previous_coup()
                  info += f"Gain réduisant la perte sur S{sixain}. Retour au coup {game.current_coup}.\n"
              else:
                  info += f"Déjà au premier coup pour S{sixain}. On reste au coup {game.current_coup}.\n"
          else:
              # Perte qui augmente
              game.next_coup()
              info += f"Perte sur S{sixain}. Passage au coup {game.current_coup}.\n"
      elif game.balance == 0:
          info += f"Équilibre sur S{sixain}. On reste au coup {game.current_coup}.\n"
      elif game.balance > 0 and not game.is_profitable():
          if game.current_coup > 1:
              game.previous_coup()
              info += f"Gain mais pas encore bénéficiaire sur S{sixain}. Retour au coup {game.current_coup}.\n"
          else:
              info += f"Déjà au premier coup pour S{sixain}. On reste au coup {game.current_coup}.\n"
      else:  # game.is_profitable()
          del self.active_games[sixain]
          info += f"Bénéfice réalisé pour S{sixain}. Fin du jeu sur ce sixain.\n"
      
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
               f"Coup actuel : {game.current_coup} (Multiplicateur : x{game.bet_progression[game.current_coup - 1]})\n" \
               f"Balance du sixain : {arrondir(game.balance)}€ ({game.get_status()})\n"

    def reset_game(self):
        self.__init__()

    def is_initialized(self):
        return self.initialized