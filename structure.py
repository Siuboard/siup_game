from board import Board
from newplayer import Player
import supporting_functions as game

board = Board()
NUMBER_OF_PAWNS_PER_PLAYER = 4
NUMBER_OF_MOVES_PER_PLAYER = 4


class Structure:
    def __init__(self):
        self.fields, self.blocks = board.fields, board.blocks
        self.number_of_players = game.get_number_of_players()
        self.list_of_players = []
        self.create_objects_of_players()
        self.create_objects_of_pawns_for_each_player()
        self.current_player = None
        self.next_player()
        self.current_winner = (0, 0)
        self.queue_to_goal = {x: [] for x in range(1, self.number_of_players + 1)}
        self.full_game()

    def create_objects_of_players(self):
        for i in range(1, self.number_of_players + 1):
            name_of_player = input('Player no.{}, please enter your name: '.format(i))
            self.list_of_players.append(Player(i, name_of_player))

    def create_objects_of_pawns_for_each_player(self):
        for player in self.list_of_players:
            player.create_pawn_obj(NUMBER_OF_PAWNS_PER_PLAYER)
            self.set_pawns_to_start_points(player)

    def set_pawns_to_start_points(self, player):
        for number, point in enumerate(board.start_points, 1):
            player.pawns[number].current_position = point

    def next_player(self):
        self.current_player = self.list_of_players.pop(0)
        self.list_of_players.append(self.current_player)

    def full_game(self):
        while True:
            self.next_player()
            self.one_round()

    def one_round(self):
        print(self.current_player.name, 'zaczyna')
        moves_comited = 0
        while moves_comited < NUMBER_OF_MOVES_PER_PLAYER:
            while self.queue_to_goal[self.current_player.id]:
                self.queue_to_goal[self.current_player.id].pop()
                self.current_player.pawns_in_goal += 1
                self.check_winner(self.current_player)

            actionable_pawn_list = []
            for pawn_id, pawn in self.current_player.pawns.items():
                if pawn.is_action_available(self.fields, self.blocks):
                    actionable_pawn_list.append(pawn_id)

            if actionable_pawn_list:
                for pawn in actionable_pawn_list:
                    print(pawn, ':', self.current_player.pawns[pawn].possibilities)
                selected_pawn = self.current_player.pawns[game.select_pawn(actionable_pawn_list)]
                x, y, action = game.select_action(selected_pawn)
                self.action(x, y, action, selected_pawn)
                moves_comited += 1
                print('current winner : ', self.current_winner)
            else:
                print(self.current_player.name, ' loose')
                self.list_of_players.pop()
                del self.current_player
                break

    def action(self, x, y, action, selected_pawn):
        print(self.current_player.name)
        if action == 'move':
            if (x, y) == board.stop_point:
                self.move_to_goal(selected_pawn.id, self.current_player)
                self.current_player.pawns_in_goal += 1
                self.check_winner(self.current_player)
            else:
                self.move_obj(selected_pawn, x, y, None, None)
                if (x, y) in board.last_points and all(self.fields[point].obj for point in board.last_points):
                    self.all_in()
                if not selected_pawn.access_to_specials:
                    for pawn_id, pawn in self.current_player.pawns.items():
                        pawn.access_to_specials = False

                selected_pawn.access_to_specials = True
        else:
            print(selected_pawn.possibilities[action][(x, y)])
            new_x, new_y = game.select_point(action, selected_pawn.possibilities[action][(x, y)],
                                             'Select coordinators where you want to '
                                             'move your {} block'.format(action))
            self.move_obj(self.blocks[(x, y)], new_x, new_y, x, y)
            selected_pawn.access_to_specials = False

    def move_obj(self, moving_obj, move_to_x, move_to_y, old_x, old_y):
        if 'pawn' not in moving_obj.type:
            self.blocks[(move_to_x, move_to_y)] = moving_obj
            self.blocks[(old_x, old_y)] = None
        self.fields[moving_obj.current_position].obj = None
        self.fields[(move_to_x, move_to_y)].obj = moving_obj.type
        moving_obj.current_position = (move_to_x, move_to_y)

    def all_in(self):
        for point in board.last_points:
            pawn_id, owner_id = tuple(self.fields[point].obj.strip('pawn'))
            pawn_id, owner_id = int(pawn_id), int(owner_id)

            if owner_id == self.current_player.id:
                self.move_to_goal(pawn_id, self.current_player)
                self.current_player.pawns_in_goal += 1
                self.check_winner(self.current_player)

            else:
                for player in self.list_of_players:
                    if player.id == owner_id:
                        self.move_to_goal(pawn_id, player)
                        self.queue_to_goal[owner_id].append(pawn_id)
                        break

    def move_to_goal(self, pawn_id, player):
        pawn = player.pawns[pawn_id]
        self.fields[pawn.current_position].obj = None
        del player.pawns[pawn_id]

    def check_winner(self, player):
        print(player.name, 'have', player.pawns_in_goal)
        if self.current_winner[1] < player.pawns_in_goal:
            self.current_winner = (player.name, player.pawns_in_goal)
        if self.current_winner[1] == NUMBER_OF_PAWNS_PER_PLAYER:
            print('Winner is : {}'.format(player.name))
            exit()


Structure()
