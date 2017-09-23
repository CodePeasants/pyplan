# Python standard library
import inspect

# Package
from plan.abstract_report import AbstractReport
from plan.abstract_stash import AbstractStash


class PluginRegistry:

    REPORT = set()
    STASH = None

    @classmethod
    def register(cls, other):
        mro = inspect.getmro(other)
        if AbstractReport in mro:
            cls.REPORT.add(other)
        elif AbstractStash in mro:
            cls.STASH = other
        else:
            raise TypeError('{} of type {} cannot be registered.'.format(other, type(other)))

    @classmethod
    def de_register(cls, other):
        mro = inspect.getmro(other)
        if AbstractReport in mro:
            if other in cls.REPORT:
                cls.REPORT.remove(other)
        elif AbstractStash in mro:
            cls.STASH = None
        else:
            raise TypeError('{} of type {} cannot be registered.'.format(other, type(other)))


class RegisterMeta(type):

    def __new__(cls, cls_name, bases, attrs):
        result = super().__new__(cls, cls_name, bases, attrs)
        PluginRegistry.register(result)
        return result
