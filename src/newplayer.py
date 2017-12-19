from pawn import Pawn


class Player:
    def __init__(self, player_id, name):
        self.id, self.name = player_id, name
        self.pawn_first_positions = [None]
        self.pawn_selected = None
        self.pawn_with_access_to_specials = None
        self.pawns_in_goal = 0
        self.pawns = {}

    def create_pawn_obj(self, NUMBER_OF_PAWNS_PER_PLAYER):
        self.pawns = dict(zip(list(range(1, NUMBER_OF_PAWNS_PER_PLAYER + 1)),
                              [Pawn(i, self.id) for i in range(1, NUMBER_OF_PAWNS_PER_PLAYER + 1)]))
