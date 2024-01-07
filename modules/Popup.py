import tkinter as tk
from tkinter import simpledialog
    
class Popup(simpledialog.Dialog):
    def __init__(self, parent, title, prompt):
        self.prompt = prompt
        super().__init__(parent, title=title)

    def body(self, master):
        tk.Label(master, text=self.prompt, font=("Helvetica", 12)).pack(pady=10)

    def buttonbox(self):
        box = tk.Frame(self)
        yes_button = tk.Button(box, text="Yes", width=10, command=self.yes_action, default=tk.ACTIVE)
        no_button = tk.Button(box, text="No", width=10, command=self.no_action)
        yes_button.pack(side="left", padx=5)
        no_button.pack(side="left", padx=5)
        box.pack()

    def yes_action(self):
        self.result = True
        self.cancel()

    def no_action(self):
        self.result = False
        self.cancel()

    def show(self):
        # reset the result before showing the dialog
        self.result = None
        super().show()
