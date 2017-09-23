# Package
from plan.serializable import Serializable


class User(Serializable):

    def __init__(self, name=None, **kwargs):
        super().__init__()
        self.name = name
        self.data = kwargs

    @classmethod
    def from_dict(cls, data):
        result = super().from_dict(data)
        result.name = data.pop('name')
        result.data = data
        return result

    def to_dict(self):
        result = super().to_dict()
        result.update(self.data)
        result['name'] = self.name
        return result
