# Python
import abc

# Package
from plan.member import Status
from plan.plugin_registry import PluginRegistry


class AbstractReport(metaclass=abc.ABCMeta):

    def __init__(self, event, title='', message='', audience=Status.GENERAL):
        self.event = event
        self.title = title
        self.message = message
        self.audience = audience

    def to_dict(self):
        return {
            'title': self.title,
            'message': self.message,
            'audience': self.audience
        }

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
