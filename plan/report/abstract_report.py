# Python
import abc

# Package
from plan.member import Status


class AbstractReport(metaclass=abc.ABCMeta):

    def __init__(self, event, title='', message='', audience=Status.GENERAL):
        self.event = event
        self.title = title
        self.message = message
        self.audience = audience

    def encode(self):
        return {
            'title': self.title,
            'message': self.message,
            'audience': self.audience
        }

    def get_members(self):
        """Get the event members this report is targetting."""
        return self.event.registrar.get(status=self.audience)

    @abc.abstractmethod
    def get_targets(self):
        """Get explicit output stream(s) for the send method."""
        pass

    @abc.abstractmethod
    def formatted(self):
        pass

    @abc.abstractmethod
    def send(self):
        pass
