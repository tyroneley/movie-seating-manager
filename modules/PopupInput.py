import tkinter as tk
from tkinter import simpledialog

class PopupInput(simpledialog.Dialog):
    def __init__(self, parent, title, prompt):
        self.prompt = prompt
        super().__init__(parent, title=title)

    def body(self, master):
        tk.Label(master, text=self.prompt, font=("Helvetica", 12)).pack(pady=10)
        self.result_var = tk.StringVar()
        entry = tk.Entry(master, textvariable=self.result_var, font=("Helvetica", 12))
        entry.pack(pady=10)
        return entry
    
    def apply(self):
        result = self.result_var.get()
        self.result = result  # set result to the entered name

