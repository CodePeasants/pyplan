# Package
from plan.member import Status
from plan.serializable import Serializable
from plan.plugin_registry import PluginRegistry
from plan.object_registry import ObjectRegistry


class Report(Serializable):

    def __init__(self, title='', message='', audience=Status.GENERAL):
        super().__init__()
        self.title = title
        self.message = message
        self.audience = audience

    def to_dict(self):
        result = super().to_dict()
        result['event'] = self.event.id
        result['title'] = self.title
        result['message'] = self.message
        result['audience'] = self.audience.value
        return result

    @classmethod
    def from_dict(cls, data):
        result = super().from_dict(data)
        result.event = ObjectRegistry.get(data.get('event'))
        result.title = data.get('title')
        result.message = data.get('message')
        result.audience = data.get('audience')
        return result

    @staticmethod
    def get_type(data):
        """Given a dictionary of serialized report data, get the AbstractReport sub-class to load the data with."""
        class_name = data.pop('__type__')
        for cls in PluginRegistry.REPORT:
            if cls.__name__ == class_name:
                return cls
