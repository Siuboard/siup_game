class Pawn:
    def __init__(self, pawn_id, owner_id):
        self.id = pawn_id
        self.owner = owner_id
        self.current_position = None
        self.access_to_specials = False
        self.type = 'pawn{}{}'.format(self.id, self.owner)
        self.possibilities = None
        self.is_actionable = False

    def is_action_available(self, fields, blocks):
        self.is_actionable = False
        self.possibilities = {
            'move': [],
            'white': {},
            'yellow': {},
            'blue': {}
        }
        neighbours = fields[self.current_position].neighbours
        for neighbour in neighbours:

            if not fields[neighbour].obj and fields[neighbour].access_for_pawns:
                self.possibilities['move'].append(neighbour)
                self.is_actionable = True

            elif fields[neighbour].obj == 'white':
                self.possibilities['white'][neighbour] = [x for x in blocks[neighbour].move_ability(neighbour, fields)]
                if self.possibilities['white'][neighbour]:
                    self.is_actionable = True

            elif fields[neighbour].obj == 'yellow' and self.access_to_specials:
                self.possibilities['yellow'][neighbour] = [x for x in blocks[neighbour].move_ability(neighbour, fields)]
                if self.possibilities['yellow'][neighbour]:
                    self.is_actionable = True

            elif fields[neighbour].obj == 'blue' and self.access_to_specials:
                blue_blocks = [point for point in [coordinates for coordinates, block in blocks.items()
                               if block and coordinates not in neighbours] if blocks[point].type == 'blue']
                for point in blue_blocks:
                    self.possibilities['blue'][point] = [x for x in blocks[point].move_ability(point, fields)]
                    if not self.is_actionable and self.possibilities['blue'][point]:
                        self.is_actionable = True

        return True if self.is_actionable else False
