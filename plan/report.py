# Package
from plan.member import Status
from plan.serializable import Serializable
from plan.plugin_registry import PluginRegistry


class Report(Serializable):

    def __init__(self, title='', message='', audience=Status.GENERAL):
        super().__init__()
        self.title = title
        self.message = message
        self.audience = audience

    @staticmethod
    def get_type(data):
        """Given a dictionary of serialized report data, get the AbstractReport sub-class to load the data with."""
        class_name = data.pop('__type__')
        for cls in PluginRegistry.REPORT:
            if cls.__name__ == class_name:
                return cls
