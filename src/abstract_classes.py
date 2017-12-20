from abc import ABCMeta, abstractmethod


class AbstractFieldState(metaclass=ABCMeta):

    @abstractmethod
    @classmethod
    def use(cls, field, pawn):
        pass

    def is_usable(self):
        pass


class Block(metaclass=ABCMeta):

    pass
