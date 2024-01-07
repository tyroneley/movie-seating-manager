from modules.Seat import Seat

class SeatsManager:
    def __init__(self, rows, cols):
        # init the seating arrangement with seat objects
        self.rows = rows
        self.cols = cols
        self.middle_rows = self.calculate_middle_rows()
        self.middle_cols = self.calculate_middle_cols()
        self.last_rows = self.calculate_last_rows()
        self.seating_grid = [[Seat(row, col, self.calculate_price(row, col)) for col in range(cols)] for row in range(rows)]

    def calculate_middle_rows(self):
        middle_index = self.rows // 2
        middle_numbers = list(range(max(1, middle_index - 2), min(self.rows + 1, middle_index + 3)))
        return middle_numbers    

    def calculate_middle_cols(self):
        middle_index = self.cols // 2
        middle_numbers = list(range(max(1, middle_index - 2), min(self.cols + 1, middle_index + 3)))
        return middle_numbers
    
    def calculate_last_rows(self):
        last_rows = [num for num in range(max(1, self.rows - 1), self.rows + 1) if num not in self.middle_rows]
        return last_rows

    def calculate_price(self, row, col):
        if row in self.middle_rows:
            if col in self.middle_cols:
                return 30
            return 20
        if row in self.last_rows:
            if col in self.middle_cols:
                return 25
            return 20
        if row > self.rows / 2:
            return 30
        return 10
            
    def display_seating(self):
        # display the current seating arrangement
        for row in self.seating_grid:
            print(' | '.join([seat.display_info() for seat in row]))
            print()
    
    def get_seating(self):
        return self.seating_grid
    
    def get_seat(self, row, col):
        seat = self.seating_grid[row][col]
        return seat

    def book_seat(self, row, col, occupant_name):
        # book a seat at the specified row and col for the given occupant
        seat = self.seating_grid[row][col]
        if not seat.is_taken:
            seat.book(occupant_name)
            print(f"Seat booked for {occupant_name} at {seat.display_info()}")
        else:
            print(f"Seat at {seat.display_info()} is already taken.")

    def display_occupants(self):
        # display the names of people occupying seats
        for row in self.seating_grid:
            for seat in row:
                if seat.is_taken:
                    print(f"{seat.occupant_name} is seated at {seat.display_info()}")
        print()

    def read_from_file(self, seating_file, occupants_file):
        # read the initial seating arrangement from the seating file
        with open(seating_file, 'r') as file:
            for row, line in enumerate(file):
                for col, seat_status in enumerate(line.strip()):
                    price = self.calculate_price(row, col)
                    self.seating_grid[row][col] = Seat(row, col, price)

        # read the occupants from the occupants file
        with open(occupants_file, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) >= 3:  # ensure there are enough parts to extract row, col, and occupant_name
                    row, col, occupant_name = int(parts[0]) - 1, int(parts[1]) - 1, ' '.join(parts[2:])
                    self.seating_grid[row][col].book(occupant_name)

    def write_to_file(self, occupants_file):
        # write the seating arrangement to the seating file
        #with open(seating_file, 'w') as file:
            #counter = 0
            #for row in self.seating_grid:
                #counter += 1
                #if counter == len(self.seating_grid):
                    #file.write(''.join(['O' for seat in row]))
                #else:
                   #file.write(''.join(['O' for seat in row]) + '\n')

        # write the occupants to the occupants file
        with open(occupants_file, 'w') as file:
            for seat in [seat for row in self.seating_grid for seat in row if seat.is_taken]:
                file.write(f"{seat.row + 1} {seat.col + 1} {seat.occupant_name}\n")