from plan.serializable import Serializable
from plan.reporter import Reporter
from plan.event import Event
from plan.settings import ID_KEY


class Manager(Serializable):

    def __init__(self, events=None, reporter=None):
        self.events = events or []
        self.__reporter = reporter

    @property
    def reporter(self):
        if not self.__reporter:
            self.__reporter = Reporter(self)
        return self.__reporter

    @classmethod
    def from_dict(cls, data):
        obj_id = data.pop(ID_KEY)
        result = cls()
        result.id = obj_id

        result.events = [Event.from_dict(x) for x in data.get('events', {})]
        result.reporter = Reporter.from_dict(data.get('reporter', {}))
        return result

    def to_dict(self):
        result = super().to_dict()
        result.update({'events': [x.to_dict() for x in self.events], 'reporter': self.reporter.to_dict()})
        return result
