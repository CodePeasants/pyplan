from enum import Enum
from enum import auto


class Status(Enum):
    INVITED = auto()
    NOT_INVITED = auto()
    PARTICIPATING = auto()
    DECLINED = auto()
    SUBSCRIBED = auto()
    BANNED = auto()


class Member:

    def __init__(self, user, status=Status.NOT_INVITED):
        self.user = user
        self.status = status

    def __repr__(self):
        return '<{0} user={1} status={2} at {3}>'.format(
            self.__class__.__name__,
            self.name,
            self.status,
            hex(id(self))
        )

    @property
    def name(self):
        return self.user.discord_name
