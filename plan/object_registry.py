# Python standard library
import weakref
from functools import partial


class ObjectRegistry:

    OBJECTS = {}

    @classmethod
    def register(cls, obj):
        obj_id = obj.id
        if obj_id not in cls.OBJECTS:
            cls.OBJECTS[obj_id] = weakref.proxy(obj, partial(cls._cleanup, obj_id))

    @classmethod
    def get(cls, obj_id):
        result = cls.OBJECTS.get(obj_id)
        if result is None:
            raise LookupError('Object with ID: {} does not exist.'.format(obj_id))
        return result

    @classmethod
    def _cleanup(cls, obj_id, ref):
        """
        Registered as a on-delete callback to the weakreference, so we don't end up with a dictionary full of keys
        pointing to dead references.
        """
        if obj_id in cls.OBJECTS:
            del cls.OBJECTS[obj_id]
