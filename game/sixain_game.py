from utils.calculations import get_douzaine_from_sixain, get_colonne_from_sixain

class SixainGame:
    def __init__(self, sixain, base_mise):
        self.sixain = sixain
        self.douzaine = (sixain - 1) // 2 + 1
        self.colonne = sixain % 3 if sixain % 3 != 0 else 3
        self.base_mise = base_mise
        self.current_coup = 1
        self.last_bet = base_mise

    def next_coup(self):
        self.current_coup += 1
        self.last_bet = self.calculate_bet()

    def reset_coup(self):
        self.current_coup = 1
        self.last_bet = self.base_mise

    def calculate_bet(self):
        return self.base_mise * (2 ** (self.current_coup - 1))

    def update_mises(self, total_mise):
        self.last_bet = total_mise / 3