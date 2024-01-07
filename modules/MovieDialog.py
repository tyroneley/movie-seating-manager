import tkinter as tk

class MovieDialog:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("New Movie")

        self.movie_name_var = tk.StringVar()
        self.rows_var = tk.StringVar()
        self.cols_var = tk.StringVar()

        tk.Label(self.top, text="Movie Name: ", font="Helvetica, 12").grid(row=0, column=0, sticky="e")
        tk.Label(self.top, text="Rows: ", font="Helvetica, 12").grid(row=1, column=0, sticky="e")
        tk.Label(self.top, text="Columns: ", font="Helvetica, 12").grid(row=2, column=0, sticky="e")

        tk.Entry(self.top, textvariable=self.movie_name_var).grid(row=0, column=1)
        tk.Entry(self.top, textvariable=self.rows_var).grid(row=1, column=1)
        tk.Entry(self.top, textvariable=self.cols_var).grid(row=2, column=1)

        tk.Button(self.top, text="OK", command=self.ok).grid(row=3, column=0, columnspan=2, pady=10)

        # centering the window
        self.top.update_idletasks()
        screen_width = self.top.winfo_screenwidth()
        screen_height = self.top.winfo_screenheight()
        x_position = (screen_width - self.top.winfo_width()) // 2
        y_position = (screen_height - self.top.winfo_height()) // 2
        self.top.geometry(f"+{x_position}+{y_position}")

    def ok(self):
        self.top.destroy()

    def get_movie_name(self):
        return self.movie_name_var.get()

    def get_rows(self):
        try:
            return int(self.rows_var.get())
        except ValueError:
            return None

    def get_cols(self):
        try:
            return int(self.cols_var.get())
        except ValueError:
            return None