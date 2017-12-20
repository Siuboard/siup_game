class Field:
    def __init__(self, position, board_size, access_for_blocks, access_for_pawns, state=None):
        self._position = position
        self._x = position[0]
        self._y = position[1]
        self._board_size = board_size
        self._neighbours = self.get_neighbours()
        self._access_for_block = access_for_blocks
        self._access_for_pawns = access_for_pawns
        self.state = state

    def get_neighbours(self):
        real_neighbours = list()
        potential_neighbours = [(self._x + 1, self._y),
                                (self._x - 1, self._y),
                                (self._x, self._y + 1),
                                (self._x, self._y - 1)]
        # checking if potential neighbours include in board
        for (x, y) in potential_neighbours:
            if 0 <= x < self._board_size and 0 <= y < self._board_size:
                real_neighbours.append((x, y))

        return real_neighbours

    def state_change(self, state, field):
        self.state = state
        field.state = None

    def state_move(self, to_field):
        if self.state:
            to_field.state_change(self.state, self)

    def request(self):
        self.state.use(self)


if __name__ == '__main__':
    f = Field((1, 0), 11)
    print(f._neighbours)

# Below Old Implementation, after tests to remove

"""class Field:

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
"""
