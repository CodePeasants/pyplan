"""
Channels transmit reports to event members. You may create your own channel types (e.g. email, sms, etc...) by
inheriting this interface and using the plugin metaclass.
"""

# Python
import weakref
import abc

# Package
from plan.serializable import Serializable
from plan.serializable import reference
from plan.plugin_registry import PluginRegistry


class AbstractChannel(Serializable, metaclass=abc.ABCMeta):

    def __init__(self, event=None):
        super().__init__()
        self.__event = None
        self.event = event

    @reference
    def event(self):
        return self.__event

    @event.setter
    def event(self, value):
        try:
            self.__event = weakref.proxy(value)
        except TypeError:
            # If the value is a basic data type (e.g. str ID) or already a weak reference.
            self.__event = value

    def get_members(self, report):
        """
        Get the event members the report is targetting.

        :param AbstractReport report:
            Report to get members for.
        """
        return self.event.registry.get(status=report.audience)

    @abc.abstractmethod
    def get_targets(self, report):
        """
        Get explicit member addresses for the send method (e.g. email addresses).

        :param AbstractReport report:
            Report to get addresses for.
        """
        pass

    @abc.abstractmethod
    def render(self):
        """
        Format the report for transmission. E.g. convert to XML embed for email, make title bold, etc...
        """
        pass

    @abc.abstractmethod
    def send(self):
        """Transmit report."""
        pass

    @staticmethod
    def get_type(data):
        """Given a dictionary of serialized report data, get the AbstractReport sub-class to load the data with."""
        class_name = data.pop('__type__')
        for cls in PluginRegistry.REPORT:
            if cls.__name__ == class_name:
                return cls
