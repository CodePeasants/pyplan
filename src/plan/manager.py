from lib import Singleton
from plan.event import Event
from plan.reporter import Reporter


class Manager(metaclass=Singleton):

    def __init__(self):
        self.__events = set()
        self.__is_dirty = True
        self.__reporter = Reporter()
        self.__reporter.start()

    @property
    def events(self):
        return list(self.__events)

    def add(self, event):
        if not isinstance(event, Event):
            raise TypeError('{0} of type: {1} must be Event!'.format(event, type(event)))
        self.__events.add(event)

    def remove(self, event):
        if not isinstance(event, Event):
            raise TypeError('{0} of type: {1} must be Event!'.format(event, type(event)))
        if event in self.__events:
            self.__events.remove(event)

    def clear(self):
        self.__events = set()
