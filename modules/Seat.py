class Seat:
    def __init__(self, row, col, price):
        self.row = row
        self.col = col
        self.price = price
        self.is_taken = False
        self.occupant_name = ""

    def book(self, occupant_name):
        self.is_taken = True
        self.occupant_name = occupant_name

    def display_info(self):
        status = "Taken" if self.is_taken else "Open"
        return f"Seat at row {self.row + 1}, col {self.col + 1}: {status} ({self.price} USD)"
