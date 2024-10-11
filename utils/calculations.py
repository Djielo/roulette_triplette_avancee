def arrondir(valeur: float) -> str:
    return f"{valeur:.2f}"

def get_sixain(number: int) -> int:
    if number == 0 or number == 37:  # 37 represents 00
        return None
    return (number - 1) // 6 + 1 if 1 <= number <= 36 else None

def get_douzaine(number: int) -> int:
    if number == 0 or number == 37:  # 37 represents 00
        return None
    return (number - 1) // 12 + 1 if 1 <= number <= 36 else None

def get_colonne(number: int) -> int:
    if number == 0 or number == 37:  # 37 represents 00
        return None
    return (number - 1) % 3 + 1 if 1 <= number <= 36 else None

def get_douzaine_from_sixain(sixain: int) -> int:
    return (sixain - 1) // 2 + 1 if sixain is not None and 1 <= sixain <= 6 else None

def get_colonne_from_sixain(sixain: int) -> int:
    if sixain is None or sixain < 1 or sixain > 6:
        return None
    return [2, 1, 3, 2, 1, 3][sixain - 1]

def calculate_gain(sixain_win: bool, douzaine_win: bool, colonne_win: bool, mise: float) -> float:
    return mise * (6 * sixain_win + 3 * douzaine_win + 3 * colonne_win)

def arrondir(valeur: float) -> float:
    return round(valeur, 2)