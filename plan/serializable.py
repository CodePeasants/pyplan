# Python standard library
import abc
import hashlib

# Package
from plan.lib import abstract_classmethod
from plan.object_registry import ObjectRegistry
from plan.settings import ID_KEY


class Serializable(metaclass=abc.ABCMeta):

    def __init__(self):
        self.__id = None

    @property
    def id(self):
        if self.__id is None:
            self.id = hashlib.md5().hexdigest()
        return self.__id

    @id.setter
    def id(self, value):
        if self.__id is not None:
            raise RuntimeError('Cannot set ID for object {} more than once!'.format(self))
        self.__id = value
        ObjectRegistry.register(self)

    @abstract_classmethod
    def from_dict(cls, data):
        result = cls()
        obj_id = data.pop(ID_KEY)
        result.id = obj_id
        return result

    @abc.abstractmethod
    def to_dict(self):
        return {ID_KEY: self.id}
