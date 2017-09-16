# Standard Library
import abc


class AbstractUser(metaclass=abc.ABCMeta):

    def __init__(self, name):
        self.name = name
