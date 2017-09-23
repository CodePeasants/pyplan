from plan.serializable import Serializable
from plan.reporter import Reporter
from plan.event import Event


class Manager(Serializable):

    def __init__(self, events=None, reporter=None):
        self.events = events or []
        self.reporter = reporter or Reporter()

    @classmethod
    def from_dict(cls, data):
        return cls(
            events=[Event.from_dict(x) for x in data.get('events', {})],
            reporter=Reporter.from_dict(data.get('reporter', {}))
        )

    def to_dict(self):
        return {'events': [x.to_dict() for x in self.events], 'reporter': self.reporter.to_dict()}
