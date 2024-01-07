import tkinter as tk
import os
from tkinter import simpledialog, messagebox
from modules.SeatsManager import SeatsManager
from modules.PopupInput import PopupInput
from modules.MovieDialog import MovieDialog

# init variables
menu_buttons = []
seating_buttons = []

# functions
def getRowsAndCols(file_name):
    with open(file_name, 'r') as file:
        content = file.read()
    lines = content.split('\n')
    rows = len(lines)
    cols = len(lines[0].strip()) # use strip as twhehe each seat (represented by Os) are concatenated in one line in the file
    return rows, cols

def create_new_movie():
    dialog = MovieDialog(window)
    window.wait_window(dialog.top)

    # get results from input
    movie_name = dialog.get_movie_name()
    rows = dialog.get_rows()
    cols = dialog.get_cols()

    if movie_name and rows is not None and cols is not None:
        new_movie_directory = "movies" 

        # create new folder for the movie
        new_movie_folder = os.path.join(new_movie_directory, movie_name)
        os.makedirs(new_movie_folder, exist_ok=True)

        # create two text files in the new folder
        with open(os.path.join(new_movie_folder, "seating.txt"), "w") as seating_file:
            counter = 0
            for row in range(rows):
                counter += 1
                if counter == rows:
                    seating_file.write(''.join(['O' for seat in range(cols)]))
                else:
                    seating_file.write(''.join(['O' for seat in range(cols)]) + '\n')
                                  
        with open(os.path.join(new_movie_folder, "occupants.txt"), "w"):
            # empty second text file for occupants
            pass

        messagebox.showinfo("Add Movie", f"The movie '{movie_name}' has been created successfully!")
        draw_menu()

def draw_menu():
    canvas.delete("all")
    for _ in range(len(seating_buttons)):
        button = seating_buttons.pop()
        button.destroy()
    for _ in range(len(menu_buttons)):
        button = menu_buttons.pop()
        button.destroy()
    
    movies_directory = "movies"
    movie_folders = [folder for folder in os.listdir(movies_directory) if os.path.isdir(os.path.join(movies_directory, folder))]

    for index, movie_folder in enumerate(movie_folders):
        button_text = f"Movie {index + 1}: {movie_folder}"
        button = tk.Button(canvas, text=button_text, width=20, height=2, command=lambda folder=movie_folder: draw_seating(folder))
        button.place(x=50, y=index * 50 + 50)
        menu_buttons.append(button)

    new_movie_button = tk.Button(canvas, text="Add Movie", width=20, height=2, command=create_new_movie)
    new_movie_button.place(x=50, y=len(menu_buttons) * 50 + 50)
    menu_buttons.append(new_movie_button)
    
    return menu_buttons

def draw_seating(folder):
    # clearing the menu
    canvas.delete("all")
    for _ in range(len(menu_buttons)):
        button = menu_buttons.pop()
        button.destroy()

    # getting seating info from the rows and cols
    rows, cols = getRowsAndCols(f"movies/{folder}/seating.txt")
    seats = SeatsManager(rows, cols)
    seats.read_from_file(f"movies/{folder}/seating.txt", f"movies/{folder}/occupants.txt")
    screen_width = 500  
    screen_height = 30
    canvas.create_rectangle(0, 0, screen_width, screen_height, fill="black")
    canvas.create_text(screen_width // 2, screen_height // 2, text="Screen", fill="white", font=("Helvetica", 12))
    
    seat_width = 30
    seat_height = 30
    gap = 5

    total_seats_width = cols * seat_width + (cols - 1) * gap
    start_x = (screen_width - total_seats_width) // 2

    for row in range(rows):
        for col in range(cols):
            seat = seats.get_seat(row, col)
            
            x = start_x + col * (seat_width + gap)
            y = (row + 1) * (seat_height + gap) # skip one row to account for the screen
            color = "gray"
            activeColor = "dark gray"

            if seat.is_taken: 
                color = "red"
                activeColor = "dark red"

            # create button instead of rectangle
            button = tk.Button(canvas, text=f"{row + 1}-{col + 1}", width=2, height=1)
            button.configure(background=color, activebackground=activeColor, command=lambda seat=seat, button=button, seats=seats: seat_click(button, seat, seats))
            button.place(x=x, y=y, width=seat_width, height=seat_height)
            seating_buttons.append(button)
    
    back_button = tk.Button(canvas, text="Back", command=lambda: draw_menu())
    back_button.configure(background="gray")
    back_button.place(x=450, y=350)

    book_button = tk.Button(canvas, text="Book", command=lambda seats=seats, folder=folder: book_seat(seats, folder))
    book_button.configure(background="gray")
    book_button.place(x=400, y=350)

    seating_buttons.append(back_button)
    seating_buttons.append(book_button)
    return seating_buttons

def seat_click(button, seat, seats):
    selected_seats = seats.get_selected_seats()

    if seat in selected_seats:
        selected_seats.remove(seat)
        button.configure(background="gray")
        return

    if seat.is_taken:
        messagebox.showinfo("Seat Taken", f"This seat has already been booked by {seat.occupant_name}!")
    else:
        seats.select_seat(seat)
        button.configure(background="yellow")
        

def book_seat(seats, folder):
    selected_seats = seats.get_selected_seats()
    num_of_selected = len(selected_seats)
    if num_of_selected <= 0: return
    
    total_price = 0
    for seat in selected_seats:
        total_price += seat.price
    name_dialog = PopupInput(window, "Book Seat", f"Total Price: ${total_price}\nEnter Name: ")
    if name_dialog.result:
        for _ in range(num_of_selected):
            seat = seats.unselect_seat()
            seat.book(name_dialog.result)
        seats.write_to_file(f"movies/{folder}/occupants.txt")
        draw_seating(folder)
        
def on_exit():
    window.destroy()

# drawing
window = tk.Tk()
window.title("Movie Theater Seating")
canvas = tk.Canvas(window, width=500, height=400, bg="white")
canvas.pack(pady=10)
draw_menu()

# window
window.update_idletasks()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x_position = (screen_width - window.winfo_width()) // 2
y_position = (screen_height - window.winfo_height()) // 2
window.geometry(f"+{x_position}+{y_position}")
window.protocol("WM_DELETE_WINDOW", on_exit)
window.mainloop()