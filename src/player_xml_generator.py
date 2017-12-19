import os
import xml.etree.ElementTree as ET
import datetime

global_player_file_name = 'global_base_of_players.xml'
full_global_player_file_name = 'players/global_base_of_players.xml'

  
def directory_generator():
    if not os.path.exists('players'):
        os.mkdir('players')

  
def global_xml_player_list_generator():
    if not os.path.exists(full_global_player_file_name):
        global_root = ET.Element('players')
        global_tree = ET.ElementTree(global_root)
        global_tree.write(full_global_player_file_name)

  
def open_xml(directory):
    tree = ET.parse(directory)
    root = tree.getroot()
    return tree, root

  
def get_name(root):
    while True:
        player_name = input("Enter name to create player (min. 3  - max. 10 characters): ")
        if len(player_name) not in range(3, 11):
            print('Wrong name format')
        elif player_name in [name.get('name') for name in root.findall('player')]:
            print('Player with this name exists')
        else:
            return player_name

  
def first_player_creator(tree, root):
    player_name = get_name(root)
    player = ET.SubElement(root, 'player', id='1', name=player_name,
                           date=str(datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')))
    with open(full_global_player_file_name, 'w'):
        tree.write(full_global_player_file_name)

  
def new_player_creator():
    while True:
        tree, root = open_xml(full_global_player_file_name)
        if not root.findall('player'):
            first_player_creator(tree, root)
        decision = input('Enter "y" to create new player or some other sign to exit: ')
        if decision == "y":
            player_name = get_name(root)
            player = ET.SubElement(root, 'player', id=str(new_player_id_creator(root)), name=player_name,
                                   date=str(datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')))
            with open(full_global_player_file_name,'w'):
                tree.write(full_global_player_file_name)
        else:
            break

  
def new_player_id_creator(root):
    max_id = max([int(player.get('id')) for player in root.findall('player')])+1
    return max_id

  
def player_xml_file_generator():
    directory_generator()
    global_xml_player_list_generator()
    new_player_creator()
