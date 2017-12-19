import board_xml_generator as b_generator
import os
from field import Field
from xml.etree import ElementTree as ET
import block


class Board:
    # now program creates board obj, using values which will comes from xml file parse

    def __init__(self):
        self.doc_name = self.__get_board_name()
        # as board existing is confirmed, program takes from xml file all necessary values

        self.__parse_from_xml = ET.parse('boards/' + self.doc_name)
        __root = self.__parse_from_xml.getroot()
        self.id = int(__root.get('id'))
        self.name = __root.get('name')
        self.size = int(__root.get('size'))
        self.start_points = [tuple(int(value) for value in point.text.split(','))
                             for point in __root.findall('start_points/start_point')]
        self.first_points = [tuple(int(value) for value in point.text.split(','))
                             for point in __root.findall('first_points/first_point')]
        self.last_points = [tuple(int(value) for value in point.text.split(','))
                            for point in __root.findall('last_points/last_point')]
        self.stop_point = tuple(int(value) for value in __root.find('stop_point').text.split(','))
        self.fields = dict.fromkeys([(j,i) for j in range(self.size) for i in range(self.size)], None)
        self.put_fields_to_dict()
        self.white_blocks = [tuple(int(value) for value in point.text.split(','))
                             for point in __root.findall('blocks/white_block')]
        self.yellow_blocks = [tuple(int(value) for value in point.text.split(','))
                              for point in __root.findall('blocks/yellow_block')]
        self.blue_blocks = [tuple(int(value) for value in point.text.split(','))
                            for point in __root.findall('blocks/blue_block')]
        self.blocks = dict.fromkeys([(x,y) for x in range(self.size) for y in range(self.size)], None)
        self.put_blocks_to_dict()

    def __get_board_name(self):
        # at first user enters name of board he want to play,
        # then program is checking if this file exists
        doc_name = ''
        while not doc_name:
            doc_name = input('Enter a name of board you want to play: ') + '.xml'
            if not os.path.exists('boards/' + doc_name):
                if input('Entered board is not exist. Do you want to create it? y/n: ') == 'y':
                    doc_name = b_generator.generator()
                else:
                    print('So one more time...')
                    doc_name = ''

        return doc_name

    def put_fields_to_dict(self):
        for (x, y) in self.fields:
            self.fields[(x, y)] = Field(x, y, self.size, self.start_points,
                                        self.first_points, self.last_points, self.stop_point)

    def put_blocks_to_dict(self):
        for (x,y) in self.white_blocks:
            self.blocks[(x, y)] = block.BlockWhite((x, y), self.size)
            self.fields[(x, y)].obj = 'white'
        for (x,y) in self.yellow_blocks:
            self.blocks[(x, y)] = block.BlockYellow((x, y), self.size)
            self.fields[(x, y)].obj = 'yellow'
        for (x,y) in self.blue_blocks:
            self.blocks[(x,y)] = block.BlockBlue((x, y), self.size)
            self.fields[(x, y)].obj = 'blue'
