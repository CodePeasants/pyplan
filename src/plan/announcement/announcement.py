# Python
import abc

# Package
from enum import Flag
from enum import auto
from event.member import Status
from event.settings import EVERYONE


class AudienceType(Flag):
    """Super-set of member status enum, as flags."""
    EVERYONE = auto()
    INVITED = auto()
    NOT_INVITED = auto()
    PARTICIPATING = auto()
    DECLINED = auto()
    SUBSCRIBED = auto()


class Announcement(metaclass=abc.ABCMeta):

    def __init__(self, event, title='', message='', audience_type=AudienceType.EVERYONE):
        self.event = event
        self.title = title
        self.message = message
        self.audience_type = audience_type

    def encode(self):
        return {
            'title': self.title,
            'message': self.message,
            'audience_type': self.audience_type
        }

    def get_members(self):
        result = []
        if self.audience_type | AudienceType.EVERYONE:
            result.append(EVERYONE)

        # Get users from the event.
        # fixme audience type cannot expand status...
        member_status = [x for x in Status if x.name in [y.name for y in Status if self.audience_type | y]]
        for status in member_status:
            result.extend([x.user for x in self.event.registrar.get(status=status)])

    @abc.abstractmethod
    def get_targets(self):
        pass

    @abc.abstractmethod
    def formatted(self):
        pass

    @abc.abstractmethod
    def send(self):
        pass
