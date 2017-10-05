# Python standard library
import weakref


class ObjectRegistry:

    OBJECTS = weakref.WeakValueDictionary()

    @classmethod
    def register(cls, obj):
        cls.OBJECTS[obj.id] = obj

    @classmethod
    def get(cls, obj_id):
        result = cls.OBJECTS.get(obj_id)
        if result is None:
            raise LookupError('Object with ID: {} does not exist.'.format(obj_id))
        return result

    @classmethod
    def clear(cls):
        """Clear out the registry. Mostly just useful for testing."""
        cls.OBJECTS = weakref.WeakValueDictionary()
