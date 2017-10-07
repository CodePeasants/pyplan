# Python standard library
import weakref
import inspect
from collections import Mapping
import abc
import uuid

# Package
from plan.lib import is_id_string
from plan.object_registry import ObjectRegistry
from plan.settings import ID_KEY
from plan.settings import SUPPORTED_REFERENCE_ITERABLES


class Serializable(metaclass=abc.ABCMeta):

    def __init__(self):
        self.__id = None

    @property
    def id(self):
        if self.__id is None:
            self.id = str(uuid.uuid4())
        return self.__id

    @id.setter
    def id(self, value):
        if self.__id is not None:
            raise RuntimeError('Cannot set ID for object {} more than once!'.format(self))
        self.__id = value
        ObjectRegistry.register(self)

    @classmethod
    def from_dict(cls, data):
        kwargs = dict(data)  # Make a shallow copy, so when we pop the ID out we don't mutate the source dictionary.
        obj_id = kwargs.pop(ID_KEY)
        result = cls(**kwargs)
        result.id = obj_id
        return result

    def to_dict(self):
        arg_spec = inspect.getargspec(self.__init__)

        result = {ID_KEY: self.id}
        for key in arg_spec.args:
            if key == 'self':
                continue

            # Convert serializable references into ID's.
            value = getattr(self, key)
            if isinstance(value, Serializable):
                value = value.id

            result[key] = value
        return result


class reference(metaclass=abc.ABCMeta):
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

        self.__dirty = False

    def __lookup(self, data):
        """
        Recursively expand nested data structures from ID's into objects from the registry.
        """
        if isinstance(data, Mapping):
            return data.__class__((k, self.__lookup(v)) for k, v in data.items())
        elif isinstance(data, SUPPORTED_REFERENCE_ITERABLES):
            return data.__class__(self.__lookup(x) for x in data)
        elif isinstance(data, str):
            return self._get_reference(ObjectRegistry.get(data))
        else:
            return self._get_reference(data)

    def __has_id(self, value):
        if isinstance(value, Mapping):
            return any(self.__has_id(x) for x in value.values())
        elif isinstance(value, SUPPORTED_REFERENCE_ITERABLES):
            return any(self.__has_id(x) for x in value)
        else:
            return is_id_string(value)

    def _get_reference(self, data):
        """Makes it easy to sub-class for weak references."""
        return data

    def __get__(self, obj, cls):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError('Un-readable attribute.')

        if self.__dirty:
            self.fset(obj, self.__lookup(self.fget(obj)))
        return self.fget(obj)

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError('Cannot set attribute.')
        # todo check if an ID is included, if so set dirty.
        if not self.__dirty and self.__has_id(value):
            self.__dirty = True
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


class weak_reference(reference):

    def _get_reference(self, data):
        try:
            return weakref.proxy(data)
        except TypeError:
            return data
