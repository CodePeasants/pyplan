# Package
from plan.serializable import Serializable


class User(Serializable):

    def __init__(self, name=None, **kwargs):
        super().__init__()
        self.name = name
        self.data = kwargs
