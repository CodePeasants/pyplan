# Python standard library
import weakref
import uuid
import inspect
from collections import Mapping
import abc

# Package
from plan.object_registry import ObjectRegistry
from plan.settings import ID_KEY
from plan.settings import SUPPORTED_REFERENCE_ITERABLES


class Serializable(metaclass=abc.ABCMeta):

    def __init__(self):
        self.__id = None

    def __eq__(self, other):
        if not isinstance(other, Serializable):
            raise TypeError('Cannot check equality with {} of type {}'.format(other, type(other)))
        my_data = self.to_dict()
        other_data = other.to_dict()
        my_data.pop(ID_KEY)
        other_data.pop(ID_KEY)
        return my_data == other_data

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def id(self):
        if self.__id is None:
            self.id = get_id()
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

        # If the object we're decoding is already in memory, update the existing object instead of creating a new one.
        try:
            result = ObjectRegistry.get(obj_id)
        except LookupError:
            result = None

        if result:
            for key, value in kwargs.items():
                setattr(result, key, value)
        else:
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

    WEAK = False

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        if doc is None and fget is not None:
            doc = fget.__doc__
        self.__doc__ = doc

        self.__dirty = False

    def __get__(self, obj, cls):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError('Un-readable attribute.')

        if self.__dirty:
            self.fset(obj, expand_ids(self.fget(obj), self.WEAK))
            self.__dirty = False
        return self.fget(obj)

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError('Cannot set attribute.')
        # todo check if an ID is included, if so set dirty.
        if not self.__dirty and has_id(value):
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

    WEAK = True


def get_id():
    """Get a valid Serializable object ID."""
    return str(uuid.uuid4())


def is_id(value):
    """Check if the provided string is a valid ID."""
    try:
        uuid.UUID(value, version=4)
    except (ValueError, AttributeError, TypeError):
        return False
    else:
        return True


def expand_ids(data, weak=False):
    """
    Recursively expand nested data structures from ID's into objects from the registry.

    :param object data:
        ID string, Serializable object or supported collection type that contains one or more of these.
    :param bool weak:
        If True, will try to return a weak reference to the expanded object instead of a strong reference.
    """
    def _return(return_data):
        if weak:
            try:
                return weakref.proxy(return_data)
            except TypeError:
                return return_data
        return return_data

    if isinstance(data, Mapping):
        return data.__class__((k, expand_ids(v, weak)) for k, v in data.items())
    elif isinstance(data, SUPPORTED_REFERENCE_ITERABLES):
        return data.__class__(expand_ids(x, weak) for x in data)
    elif is_id(data):
        return _return(ObjectRegistry.get(data))
    else:
        return _return(data)


def has_id(data):
    """
    Check if the provided data is or has a Serializable ID.

    :param object data:
        ID string, Serializable object or supported collection type that contains one or more of these.
    :rtype bool:
    """
    if isinstance(data, Mapping):
        return any(has_id(x) for x in data.values())
    elif isinstance(data, SUPPORTED_REFERENCE_ITERABLES):
        return any(has_id(x) for x in data)
    else:
        return is_id(data)
