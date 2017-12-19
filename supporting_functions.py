def get_number_of_players():
    try:
        number_of_players = int(input('Enter number of players: '))
    except ValueError:
        print('It is not integer')
        return get_number_of_players()
    else:
        return number_of_players


def select_pawn(actionable_pawns):
    try:
        chosen_id_of_pawn = int(input('Enter number of pawn you want to use: '))
    except ValueError:
        print('Wrong number')
        return select_pawn(actionable_pawns)
    else:
        if chosen_id_of_pawn in actionable_pawns:
            return chosen_id_of_pawn
        else:
            return select_pawn(actionable_pawns)


def select_action(pawn):
    print(pawn.possibilities)
    action = input('Choose action: ')
    if action in pawn.possibilities:
        try:
            x, y = input('Enter coordinates you want to use(ie. "1 2"): ').split(' ')
            x, y = int(x), int(y)
        except ValueError:
            print('Wrong input')
            return select_action(pawn)
        else:
            if (x, y) in pawn.possibilities[action]:
                return x, y, action
            else:
                return select_action(pawn)
    else:
        return select_action(pawn)


def select_point(action, possibilities, text):
    try:
        where_to_x, where_to_y = input(text).split(' ')
        where_to_x, where_to_y = int(where_to_x), int(where_to_y)
    except ValueError:
        print('Wrong input')
        return select_point(action, possibilities, text)
    else:
        return where_to_x, where_to_y if (where_to_x, where_to_y) in possibilities \
            else select_point(action, possibilities, text)
