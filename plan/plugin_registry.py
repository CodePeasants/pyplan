# Python standard library
import inspect

# Package
from plan.exceptions import PluginNameClashError
from plan.exceptions import PluginNotFoundError


class PluginRegistry:

    PLUGINS = {}
    __VALID_TYPES = ('Report', 'AbstractStash', 'AbstractChannel')

    @classmethod
    def register(cls, other):
        mro = [x.__name__ for x in inspect.getmro(other)]

        # Ensure that the registered class is of a valid type.
        if not any(x in mro for x in cls.__VALID_TYPES):
            raise TypeError(f'{other} of type {type(other)} cannot be registered.')

        # Cannot have clashing plugin names.
        if other.__name__ in cls.PLUGINS:
            raise PluginNameClashError(
                f'Cannot register: {other}. A plugin with the same name: {other.__name__}'
                ' is registered: {cache.get(other.__name__)}'
            )

        cls.PLUGINS[other.__name__] = other

    @classmethod
    def de_register(cls, other):
        if other in cls.PLUGINS.values():
            del cls.PLUGINS[other.__name__]
        else:
            raise PluginNotFoundError(f'{other} of type {type(other)} is not a registered plugin!')

    @classmethod
    def get(cls, type_str):
        result = cls.PLUGINS.get(type_str)
        if result is None:
            raise PluginNotFoundError(f'Plugin with name: {type_str} not registered.')
        return result


class RegisterMeta(type):

    def __new__(cls, cls_name, bases, attrs):
        result = super().__new__(cls, cls_name, bases, attrs)
        PluginRegistry.register(result)
        return result
