# Python standard library
import weakref


class ObjectRegistry:

    OBJECTS = {}

    @classmethod
    def register(cls, obj):
        if obj.id not in cls.OBJECTS:
            cls.OBJECTS[obj.id] == weakref.proxy(obj)

    @classmethod
    def get(cls, obj_id):
        result = cls.OBJECTS.get(obj_id)
        if result is None:
            raise LookupError('Object with ID: {} does not exist.'.format(obj_id))
        return result
