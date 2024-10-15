from utils.calculations import get_douzaine_from_sixain, get_colonne_from_sixain

class SixainGame:
    def __init__(self, sixain, base_mise):
        self.sixain = sixain
        self.douzaine = (sixain - 1) // 2 + 1
        self.colonne = sixain % 3 if sixain % 3 != 0 else 3
        self.base_mise = base_mise
        self.current_coup = 1
        self.last_bet = base_mise
        self.bet_progression = [1, 1, 1, 2, 3, 5, 8, 15, 30]
        self.total_bet = 0
        self.total_gain = 0
        self.balance = 0

    def next_coup(self):
        if self.current_coup < 9:
            self.current_coup += 1
        self.last_bet = self.calculate_bet()

    def previous_coup(self):
        if self.current_coup > 1:
            self.current_coup -= 1
        self.last_bet = self.calculate_bet()

    def reset_coup(self):
        self.current_coup = 1
        self.last_bet = self.base_mise
        self.total_bet = 0
        self.total_gain = 0
        self.balance = 0

    def calculate_bet(self):
        return self.base_mise * self.bet_progression[self.current_coup - 1]

    def update_mises(self, total_mise):
        self.last_bet = total_mise / 3
        self.total_bet += total_mise
        self.update_balance()

    def update_gains(self, gain):
        self.total_gain += gain
        self.update_balance()

    def update_balance(self):
        self.balance = self.total_gain - self.total_bet

    def is_profitable(self):
        return self.balance > 0

    def get_status(self):
        if self.balance > 0:
            return "Bénéfice"
        elif self.balance < 0:
            return "Perte"
        else:
            return "Équilibre"