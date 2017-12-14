# Package
from plan.serializable import Serializable
from plan.reporter import Reporter
from plan.serializable import reference


class Manager(Serializable):

    def __init__(self, events=None, reporter=None):
        super().__init__()
        self.__events = events or []
        self.__reporter = reporter

    @reference
    def reporter(self):
        if not self.__reporter:
            self.__reporter = Reporter(self)
        return self.__reporter

    @reference
    def events(self):
        return self.__events
