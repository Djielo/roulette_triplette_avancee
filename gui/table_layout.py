import tkinter as tk

def create_roulette_table(parent, callback):
    parent.grid_columnconfigure(0, weight=1)
    parent.grid_rowconfigure(0, weight=1)

    table = tk.Frame(parent, bg="green")
    table.grid(sticky="nsew")

    # Create number grid
    number_frame = tk.Frame(table, bg="green")
    number_frame.grid(row=0, column=1, columnspan=12, sticky="nsew", padx=3, pady=3)

    btn_width = 4
    btn_height = 2

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
                            command=lambda x=number: callback(x),
                            width=btn_width, height=btn_height)
            btn.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)

    # Create 0 and 00 button
    zero_frame = tk.Frame(table, bg="green")
    zero_frame.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
    tk.Button(zero_frame, text="0", bg="green", fg="white", width=btn_width, 
              command=lambda: callback(0)).pack(expand=True, fill="both")
    tk.Button(zero_frame, text="00", bg="green", fg="white", width=btn_width, 
              command=lambda: callback(37)).pack(expand=True, fill="both")

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