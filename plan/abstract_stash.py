# Python standard library
import abc

# Package
from plan.lib import abstract_staticmethod


class AbstractStash(metaclass=abc.ABCMeta):

    @abstract_staticmethod
    def load(cls, **kwargs):
        pass

    @abstract_staticmethod
    def dump(manager, **kwargs):
        pass
