import tkinter as tk
from gui.roulette_gui import RouletteGUI

def main():
    root = tk.Tk()
    root.geometry("650x800")
    gui = RouletteGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()