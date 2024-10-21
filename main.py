import tkinter as tk
from gui.roulette_gui import RouletteGUI

def main():
    root = tk.Tk()
    
    # Récupérer la taille de l'écran
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Ajuster la fenêtre à 80% de la taille de l'écran
    root.geometry(f"{int(screen_width * 0.6)}x{int(screen_height * 0.8)}")
    
    # S'assurer que la fenêtre se redimensionne
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    
    # Créer l'interface avec la classe RouletteGUI
    gui = RouletteGUI(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()
