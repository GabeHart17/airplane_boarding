import random


class Passenger:
    def __init__(self, seat_row, seat_letter, has_bag=True):
        self.row = seat_row
        self.letter = seat_letter
        self.bag = has_bag
        self.bag_counter = -1
        self.seat_swap_counter = -1


class Airplane:
    def __init__(self, rows, seat_letters, aisle_pos,  # aisle_pos = number of seats left of aisle, seat_letters go left to right
                 stow_ticks=2, swap_ticks=3):
        self.left_seats = seat_letters[:aisle_pos]
        self.right_seats = seat_letters[aisle_pos:]
        self.seats = [
            {i: None for i in seat_letters}
            for j in range(rows)
        ]
        self.aisle = [None for i in range(rows)]
        self.stow = stow_ticks  # ticks required to stow bag
        self.swap = swap_ticks  # ticks required to move past 1 person to a seat

    def aisle_empty(self):
        return all([i is None for i in self.aisle])

    def update(self, next_passenger):
        next_accepted = False
        for r in range(len(self.aisle)):
            row = len(self.aisle) - 1 - r
            if self.aisle[row] is None:
                if row == 0:
                    self.aisle[row] = next_passenger
                    next_accepted = True
            else:
                passenger = self.aisle[row]
                if row == passenger.row:
                    if passenger.bag_counter < 0 and passenger.bag:
                        passenger.bag_counter = self.stow
                    elif passenger.bag_counter > 0 and passenger.bag:
                        passenger.bag_counter -= 1
                    elif passenger.bag_counter == 0 or not passenger.bag:
                        if passenger.seat_swap_counter < 0:
                            side = self.left_seats if\
                                    passenger.letter in self.left_seats\
                                    else self.right_seats
                            intermediate_seats = []
                            if side == self.left_seats:
                                intermediate_seats = self.left_seats[
                                    self.left_seats.index(passenger.letter):
                                ]
                            elif side == self.right_seats:
                                intermediate_seats = self.right_seats[
                                    :self.right_seats.index(passenger.letter)
                                ]
                            intermediate_passengers = [
                                self.seats[passenger.row][i] is not None
                                for i in intermediate_seats
                            ].count(True)
                            passenger.seat_swap_counter = \
                                self.swap * intermediate_passengers
                        elif passenger.seat_swap_counter > 0:
                            passenger.seat_swap_counter -= 1
                        elif passenger.seat_swap_counter == 0:
                            self.seats[passenger.row][passenger.letter] = \
                                passenger
                            self.aisle[row] = None
                else:
                    if self.aisle[row + 1] is None:
                        self.aisle[row + 1] = passenger
                        self.aisle[row] = None
        return next_accepted  # whether or not next_passenger was able to enter plane


class BoardingQueue:
    def __init__(self, num_rows, seat_letters, aisle_pos):
        self.rows = num_rows
        self.letters = seat_letters
        self.aisle = aisle_pos
        self.queue = self.generate_queue()
        self.pos = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.pos < len(self.queue):
            self.pos += 1
            return self.queue[self.pos - 1]
        else:
            raise StopIteration

    def generate_queue(self):
        return []


class RandomQueue(BoardingQueue):
    def __init__(self, num_rows, seat_letters, aisle_pos):
        super().__init__(num_rows, seat_letters, aisle_pos)

    def generate_queue(self):
        q = []
        for r in range(self.rows):
            for l in self.letters:
                q.append(Passenger(r, l))
        random.shuffle(q)
        return q


class EfficientQueue(BoardingQueue):
    def __init__(self, num_rows, seat_letters, aisle_pos):
        super().__init__(num_rows, seat_letters, aisle_pos)

    def generate_queue(self):
        left = self.letters[:self.aisle]
        right = self.letters[self.aisle:]
        letter_order = []
        side = True  # True is right, False is left
        while len(letter_order) < len(self.letters):
            if not left:
                letter_order.append(right.pop(-1))
            elif not right:
                letter_order.append(left.pop(0))
            else:
                letter_order.append((right if side else left).pop(-int(side)))
                side = not side
        q = []
        for l in letter_order:
            for r in range(self.rows):
                q.append(Passenger(self.rows - r - 1, l))
        return q


class InefficientQueue(BoardingQueue):
    def __init__(self, num_rows, seat_letters, aisle_pos):
        super().__init__(num_rows, seat_letters, aisle_pos)

    def generate_queue(self):
        left = self.letters[:self.aisle]
        left.reverse()
        right = self.letters[self.aisle:]
        letter_order = left + right
        q = []
        for r in range(self.rows):
            for l in letter_order:
                q.append(Passenger(r, l))
        return q


class BackToFrontQueue(BoardingQueue):
    def __init__(self, num_rows, seat_letters, aisle_pos):
        super().__init__(num_rows, seat_letters, aisle_pos)

    def generate_queue(self):
        q = []
        for r in range(self.rows):
            p = [Passenger(self.rows - r - 1, l) for l in self.letters]
            random.shuffle(p)
            for i in p:
                q.append(i)
        return q


class GroupQueue(BoardingQueue):
    def __init__(self, num_rows, seat_letters, aisle_pos, num_groups):
        self.groups = self.create_groups(num_groups, num_rows)
        super().__init__(num_rows, seat_letters, aisle_pos)

    def create_groups(self, num_groups, num_rows):
        group_size = round(num_rows / num_groups)
        g = [group_size * i for i in range(num_groups)] + [num_rows]
        return g

    def generate_queue(self):
        q = []
        for i in range(len(self.groups) - 1):
            s = []
            for r in range(self.groups[i], self.groups[i + 1]):
                for l in self.letters:
                    s.append(Passenger(r, l))
            random.shuffle(s)
            q += s
        return q


class SouthwestQueue(BoardingQueue):
    def __init__(self):
        super().__init__(30, ['A', 'B', 'C', 'D', 'E', 'F'], 3)

    def generate_queue(self):
        aisle_window = ['A', 'C', 'D', 'F']
        middle = ['B', 'E']
        aw = []
        for l in aisle_window:
            for r in range(self.rows):
                aw.append(Passenger(r, l))
        random.shuffle(aw)
        m = []
        for l in middle:
            for r in range(self.rows):
                m.append(Passenger(r, l))
        random.shuffle(m)
        return aw + m


def simulate(queue, stow, swap):
    plane = Airplane(queue.rows, queue.letters, queue.aisle,
                     stow_ticks=stow, swap_ticks=swap)
    ticks = 0
    for passenger in queue:
        while True:
            ticks += 1
            if plane.update(passenger):
                break
    while not plane.aisle_empty():
        ticks += 1
        plane.update(None)
    return ticks
