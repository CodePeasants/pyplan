# Python
import abc

# Package
from plan.member import Status
from plan.serializable import Serializable
from plan.serializable import reference
from plan.plugin_registry import PluginRegistry
from plan.object_registry import ObjectRegistry


class AbstractReport(Serializable, metaclass=abc.ABCMeta):

    def __init__(self, event=None, title='', message='', audience=Status.GENERAL):
        super().__init__()
        self.__event = None
        self.event = event
        self.title = title
        self.message = message
        self.audience = audience

    @reference
    def event(self):
        return self.__event

    @event.setter
    def event(self, value):
        self.__event = value

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

    def get_members(self):
        """Get the event members this report is targetting."""
        return self.event.registry.get(status=self.audience)

    @abc.abstractmethod
    def get_targets(self):
        """Get explicit output stream(s) for the send method."""
        pass

    @abc.abstractmethod
    def format(self):
        pass

    @abc.abstractmethod
    def send(self):
        pass

    @staticmethod
    def get_type(data):
        """Given a dictionary of serialized report data, get the AbstractReport sub-class to load the data with."""
        class_name = data.pop('__type__')
        for cls in PluginRegistry.REPORT:
            if cls.__name__ == class_name:
                return cls
