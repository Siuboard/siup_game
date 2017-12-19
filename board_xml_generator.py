import xml.etree.ElementTree as ET
import os
from slugify import slugify
from datetime import datetime

# using input values, creates necessary information and send them to xml file
base_of_boards_directory = 'boards/global_base_of_boards.xml'

block_dict = dict.fromkeys([2,3,4], None)


def read_size():
    while True:
        number = input('Set number of columns/rows, please (Only odd numbers and min. 5) : ')
        if is_int_possible(number):
            number = int(number)
            if number % 2 != 0 and number >= 3:
                return number
            else:
                print('It is not odd value or is lower then 5')
        else:
            print('It is not a integer')


def is_int_possible(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


def create_points(size):
    start_points = get_start_points(size)
    first_points = get_first_points(size)
    stop_point = get_stop_point(size)
    last_points = get_last_points(stop_point[1])
    return start_points, first_points, last_points, stop_point


def get_start_points(size):
    return [(0, 0), (0, size-1), (size-1, 0), (size-1, size-1)]


def get_first_points(size):
    return [(0, 1), (1, 0), (0, size-2), (1, size-1), (size-2, 0), (size-1, 1), (size-2, size-1), (size-1, size-2)]


def get_stop_point(size):
    return int(size//2), int(size//2)


def get_last_points(stop):
    return [(stop, stop-1), (stop, stop+1), (stop-1, stop), (stop+1, stop)]


def get_block_type():
    while True:
        block_type = input('2- White Block, \n3- Yellow Block, \n4- Blue Block \n'
                           'Please enter a number of type, or "quit" : ')
        if block_type == 'quit':
            return None
        elif is_int_possible(block_type) and block_type in ['2', '3', '4']:
            return int(block_type)
        else:
            print('Wrong input')


def get_block_coordinators(size, forbidden_points):
    while True:
        decision = input('Please enter coordinators "x,y" (eq. 1,2 ), or "quit" to exit. '
                         'Numbers should be in range 0 to {} '.format(size-1))
        if not decision or decision == "quit":
            break
        try:
            x_crd, y_crd = decision.split(',')
        except Exception:
            print('Wrong format of input')
            continue
        else:
            if all(is_int_possible(valu) for valu in [x_crd, y_crd]) and all(int(val) in range(size) for val in [x_crd, y_crd]):
                coordins = tuple(int(value) for value in [x_crd, y_crd])
                if coordins not in forbidden_points:
                    yield coordins
                else:
                    print("Point forbidden")
            else:
                print('Coordinators are not valid')


def get_blocks(size, forbidden_points):
    point_dict = {}
    while True:
        block_type = get_block_type()
        if not block_type:
            break
        else:
            block_coordins = get_block_coordinators(size, forbidden_points)
            for point in block_coordins:
                if point in point_dict:
                    del_type = point_dict[point]
                    point_dict[point] = block_type
                else:
                    point_dict[point] = block_type

    for point, point_type in point_dict.items():
        if not block_dict[point_type]:
            block_dict[point_type] = [point]
        else:
            block_dict[point_type].append(point)


def directory_creator():
    # checks if dir exist, otherwise is creating it

    if not os.path.exists('boards'):
        os.mkdir('boards')
    board_name = ''

    while not board_name:
        board_name = input('Enter a name of new board file (without blank spaces and specials): ')
        board_name = slugify(board_name)
        file_name = "{}.xml".format(board_name)

        if os.path.exists('boards/' + file_name):
            print('Board with that name exists')
            board_name = ''
        else:
            if input('Name of board is {}, and name of file is {}. It is correct? (y/n)'
                             .format(board_name, file_name)) != 'y':
                board_name = ''

    return board_name, file_name


def global_base_creator(board_name):
    if not os.path.exists(base_of_boards_directory):
        with open(base_of_boards_directory, 'w'):
            new_root = ET.Element('boards')
            new_tree = ET.ElementTree(new_root)
            max_id = '1'
            new_board = ET.SubElement(new_root, 'board', name=board_name, id=max_id, date=str(datetime.now().date()))
            new_tree.write(base_of_boards_directory)

    else:
        base__of_boards = ET.parse(base_of_boards_directory)
        new_root = base__of_boards.getroot()
        max_id = str(max([int(n_id.get('id')) for n_id in base__of_boards.findall('board')]) + 1)
        new_board = ET.SubElement(new_root, 'board', name=board_name, id=max_id, date=str(datetime.now().date()))
        base__of_boards.write(base_of_boards_directory)

    return max_id


def xml_creator(file_name, board_name, board_size, starts, firsts, lasts, stop, max_id):
    root = ET.Element("board", name=board_name, id=max_id, size=str(board_size))
    tree = ET.ElementTree(root)

    starts_element = ET.SubElement(root, 'start_points')
    for (x, y) in starts:
        start_element = ET.SubElement(starts_element, 'start_point')
        start_element.text = '{},{}'.format(str(x), str(y))

    firsts_element = ET.SubElement(root, 'first_points')
    for (x, y) in firsts:
        first_element = ET.SubElement(firsts_element, 'first_point')
        first_element.text = '{},{}'.format(str(x), str(y))

    lasts_element=ET.SubElement(root, 'last_points')
    for (x, y) in lasts:
        last_point = ET.SubElement(lasts_element, 'last_point')
        last_point.text = '{},{}'.format(str(x), str(y))

    (x, y) = stop
    stop_element = ET.SubElement(root, 'stop_point')
    stop_element.text = '{},{}'.format(str(x), str(y))

    blocks = ET.SubElement(root, 'blocks')
    if block_dict[2]:
        for (x, y) in block_dict[2]:
            white_block = ET.SubElement(blocks, 'white_block')
            white_block.text = '{},{}'.format(str(x), str(y))

    if block_dict[3]:
        for (x, y) in block_dict[3]:
            yellow_block = ET.SubElement(blocks, 'yellow_block')
            yellow_block.text = '{},{}'.format(str(x), str(y))

    if block_dict[4]:
        for (x, y) in block_dict[4]:
            blue_block = ET.SubElement(blocks, 'blue_block')
            blue_block.text = '{},{}'.format(str(x), str(y))

    with open('boards/'+file_name, 'w'):
        tree.write('boards/'+file_name)


def generator():
    board_name, file_name = directory_creator()
    max_id = global_base_creator(board_name)
    board_size = read_size()
    starts, firsts, lasts, stop = create_points(board_size)
    forbidden_points = starts + firsts + lasts + [stop]
    get_blocks(board_size, forbidden_points)
    xml_creator(file_name, board_name, board_size, starts, firsts, lasts, stop, max_id)

    return file_name
