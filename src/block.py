from src.abstract_classes import AbstractFieldState, Block
from src.board import Board


class BlockWhite(AbstractFieldState, Block):

    @classmethod
    def use(cls, field, pawn):
        cls.move_ability(field._board_size, field._position, pawn.current_position, Board.fields)


    @staticmethod
    def vector_list(current_position, pawn_position):
        pawn_x, pawn_y = pawn_position
        vector_x, vector_y = (current_position[0] - pawn_x,
                              current_position[1] - pawn_y)
        return vector_x, vector_y

    @classmethod
    def move_ability(cls, size, current_position, pawn_position, fields):
        x, y = cls.vector_list(current_position, pawn_position)
        if all(value in range(size) for value in [current_position[0] + x, current_position[1] + y]):
            field = fields[(current_position[0] + x, current_position[1] + y)]
            if field._state is None and field._access_for_blocks:
                return current_position[0] + x, current_position[1] + y


class BlockYellow(Block):

    @staticmethod
    def vector_list(current_position, pawn_position):
        for i in range(size):
            for j in range(size):
                if (current_position[0], current_position[1]) != (i, j) and \
                     fields[(i, j)].access_for_blocks and not fields[(i, j)].obj:
                    yield (i, j)


class BlockBlue(Block):

    @staticmethod
    def vector_list(current_position, pawn_position):
        for (x, y) in fields[(current_position[0], current_position[1])].neighbours:
            yield (x - current_position[0], y - current_position[1])

    @classmethod
    def move_ability(cls, size, current_position, pawn_position, fields)
        for (x, y) in self.vector_list(fields):
            current_x, current_y = current_position[0], current_position[1]
            while True:
                if current_x + x in range (size) and current_y + y in range(size):
                    f = fields[(current_x+x, current_y+y)]
                    if not f.obj and f.access_for_blocks:
                        yield (current_x+x, current_y+y)
                        current_x += x
                        current_y += y
                    else:
                        break
                else:
                    break


"""

class Block:
    def __init__(self, start_position, size):
        self.size = size
        self.current_position = start_position
        self.__need_move_to_access = False


class BlockWhite(Block):
    def __init__(self, start_position, size):
        super().__init__(start_position, size)
        self.type = 'white'

    def vector_list(self, pawn_position):
        pawn_x, pawn_y = pawn_position
        vector_x, vector_y = (self.current_position[0] - pawn_x,
                              self.current_position[1] - pawn_y)
        return vector_x, vector_y

    def move_ability(self, pawn_position, fields):
        x, y = self.vector_list(pawn_position)
        if all(value in range(self.size) for value in [self.current_position[0] + x, self.current_position[1] + y] ):
            f = fields[(self.current_position[0] + x, self.current_position[1] + y)]
            if not f.obj and f.access_for_blocks:
                return self.current_position[0] + x, self.current_position[1] + y


class BlockYellow(Block):
    def __init__(self, start_position, size):
        super().__init__(start_position, size)
        self.__need_move_to_access = True
        self.type = 'yellow'

    def move_ability(self, pawn_position, fields):
        for i in range(self.size):
            for j in range(self.size):
                if (self.current_position[0], self.current_position[1]) != (i, j) and \
                     fields[(i, j)].access_for_blocks and not fields[(i, j)].obj:
                    yield (i, j)


class BlockBlue(Block):
    def __init__(self, start_position, size):
        super().__init__(start_position, size)
        self.__need_move_to_access = True
        self.type = 'blue'

    def vector_list(self, fields):
        for (x, y) in fields[(self.current_position[0], self.current_position[1])].neighbours:
            yield (x - self.current_position[0], y - self.current_position[1])

    def move_ability(self, pawn_position, fields):
        for (x, y) in self.vector_list(fields):
            current_x, current_y = self.current_position[0], self.current_position[1]
            while True:
                if current_x + x in range (self.size) and current_y + y in range(self.size):
                    f = fields[(current_x+x, current_y+y)]
                    if not f.obj and f.access_for_blocks:
                        yield (current_x+x, current_y+y)
                        current_x += x
                        current_y += y
                    else:
                        break
                else:
                    break
"""