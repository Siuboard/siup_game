import src.board_xml_generator as b_generator
import os
from src import block
from src.field import Field
from xml.etree import ElementTree as ET


class Board:

    __root, id, name, size = None, None, None, None
    start_points, first_points, last_points, stop_point = list(), list(), list(), None
    fields = dict()
    white_blocks, yellow_blocks, blue_blocks = list(), list(), list()
    blocks = dict()

    @classmethod
    def __call__(cls, *args, **kwargs):
        cls.parse_xml(cls.__get_board_name())
        cls.points_init()
        cls.fields_init()
        cls.blocks_init()

    @classmethod
    def __get_board_name(cls):
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

    @classmethod
    def parse_xml(cls, doc_name):
        __parse_from_xml = ET.parse('boards/' + doc_name)
        cls.__root = __parse_from_xml.getroot()
        cls.id = int(cls.__root.get('id'))
        cls.name = cls.__root.get('name')
        cls.size = int(cls.__root.get('size'))

    @classmethod
    def points_init(cls):
        cls.start_points = [tuple(int(value) for value in point.text.split(','))
                            for point in cls.__root.findall('start_points/start_point')]
        cls.first_points = [tuple(int(value) for value in point.text.split(','))
                            for point in cls.__root.findall('first_points/first_point')]
        cls.last_points = [tuple(int(value) for value in point.text.split(','))
                            for point in cls.__root.findall('last_points/last_point')]
        cls.stop_point = tuple(int(value) for value in cls.__root.find('stop_point').text.split(','))

    @classmethod
    def fields_init(cls):
        cls.fields = dict.fromkeys([(j, i) for j in range(cls.size) for i in range(cls.size)], None)

        for (x, y) in cls.fields:
            cls.fields[(x, y)] = Field((x, y), cls.size,
                        [False, True][any([(x, y) in arr for arr in
                                           [cls.start_points, cls.first_points, cls.last_points]])
                                      or (x, y) == cls.stop_point],
                        [True, False][(x, y) in cls.start_points])

    @classmethod
    def blocks_init(cls):
        cls.white_blocks = [tuple(int(value) for value in point.text.split(','))
                            for point in cls.__root.findall('blocks/white_block')]
        cls.yellow_blocks = [tuple(int(value) for value in point.text.split(','))
                             for point in cls.__root.findall('blocks/yellow_block')]
        cls.blue_blocks = [tuple(int(value) for value in point.text.split(','))
                           for point in cls.__root.findall('blocks/blue_block')]

        cls.blocks = dict.fromkeys([(x, y) for x in range(cls.size) for y in range(cls.size)], None)

    # TODO decide if blocks array is needed

        for (x, y) in cls.white_blocks:
            cls.blocks[(x, y)] = 'white'
            cls.fields[(x, y)].state = block.BlockWhite
        for (x, y) in cls.yellow_blocks:
            cls.blocks[(x, y)] = 'yellow'
            cls.fields[(x, y)].obj = block.BlockYellow
        for (x, y) in cls.blue_blocks:
            cls.blocks[(x, y)] = 'blue'
            cls.fields[(x, y)].obj = block.BlockBlue
