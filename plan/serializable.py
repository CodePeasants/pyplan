# Python standard library
import abc

# Package
from plan.lib import abstract_classmethod


class Serializable(metaclass=abc.ABCMeta):

    @abstract_classmethod
    def from_dict(cls, data):
        pass

    @abc.abstractmethod
    def to_dict(self):
        pass
