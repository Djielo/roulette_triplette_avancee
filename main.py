import tkinter as tk
from gui.roulette_gui import RouletteGUI

def main():
    root = tk.Tk()
    root.geometry("1000x800")  # Ajusté pour accommoder la nouvelle interface
    gui = RouletteGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()