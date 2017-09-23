# Package
from plan.serializable import Serializable
from plan.settings import ID_KEY


class User(Serializable):

    def __init__(self, name, **kwargs):
        super().__init__()
        self.name = name
        self.data = kwargs

    @classmethod
    def from_dict(cls, data):
        obj_id = data.pop(ID_KEY)
        result = cls(data.pop('name'), **data)
        result.id = obj_id
        return result

    def to_dict(self):
        result = super().to_dict()
        result.update(self.data)
        result['name'] = self.name
        return result
