# Package
from plan.serializable import Serializable


class User(Serializable):

    def __init__(self, name, **kwargs):
        self.name = name
        self.data = kwargs

    @classmethod
    def from_dict(cls, data):
        return cls(data.pop('name'), **data)

    def to_dict(self):
        result = {'name': self.name}
        result.update(self.data)
        return result
