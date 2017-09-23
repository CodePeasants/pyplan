# Package
from plan.abstract_stash import AbstractStash
from plan.plugin_registry import RegisterMeta


class JSONStash(AbstractStash, metaclass=RegisterMeta):

    @staticmethod
    def load(**kwargs):
        pass

    @staticmethod
    def dump(manager, **kwargs):
        pass
