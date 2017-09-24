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


class serializable_reference:
    """
    All object references in this framework's object model must be decorated with this class to be serializable.
    It works like a normal property, but the getter will automatically translate ID's into objects using the
    ObjectRegistry. This enables us to de-serialize objects in any order. Otherwise if object A references object B,
    but object B has not been deserialized yet, you would get an error. This allows you to set object A's reference to
    object B as it's ID. Only when it gets called the first time will it resolve to the actual object.
    """
    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        if doc is None and fget is not None:
            doc = fget.__doc__
        self.__doc__ = doc

        self.reference = None

    def __get__(self, obj, cls):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError('Un-readable attribute.')

        result = self.fget(obj)
        if isinstance(result, str):
            if self.reference is None or self.reference.id != result:
                self.reference = ObjectRegistry.get(result)
            else:
                return self.reference
        else:
            return result

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError('Cannot set attribute.')
        self.fset(obj, value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError('Cannot delete attribute.')
        self.fdel(obj)

    def getter(self, fget):
        return type(self)(fget, self.fset, self.fdel, self.__doc__)

    def setter(self, fset):
        return type(self)(self.fget, fset, self.fdel, self.__doc__)

    def deleter(self, fdel):
        return type(self)(self.fget, self.fset, fdel, self.__doc__)
