class Field:

    def __init__(self, x, y, size, start_point_list, first_point_list, last_point_list, stop_point):
        self.x = x
        self.y = y
        self.size = size
        self.position = (self.x, self.y)
        self.access_for_blocks = [True, False][(self.position in start_point_list)
                                                or (self.position in first_point_list)
                                                or (self.position in last_point_list)
                                                or (self.position == stop_point)]
        self.access_for_pawns = [True, False][self.position in start_point_list]
        self.obj = None

    @property
    def neighbours(self):
        return list(self.get_neighbours())

    def get_neighbours(self):
        potential_neighbours = [(self.x + 1, self.y),
                                (self.x - 1, self.y),
                                (self.x, self.y + 1),
                                (self.x, self.y - 1)]
        # checking if potential neighbours include in board
        for (xn, yn) in potential_neighbours:
            if 0 <= xn < self.size and 0 <= yn < self.size: yield (xn, yn)

