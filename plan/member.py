# Python standard library
from enum import Enum
from enum import auto

# Package
from plan.serializable import Serializable
from plan.serializable import reference


class Status(Enum):
    INVITED = auto()
    NOT_INVITED = auto()
    PARTICIPATING = auto()
    DECLINED = auto()
    SUBSCRIBED = auto()
    BANNED = auto()

    # Macros for convenience.
    ALL = INVITED | NOT_INVITED | PARTICIPATING | DECLINED | SUBSCRIBED | BANNED  # All statuses.
    GENERAL = INVITED | NOT_INVITED | PARTICIPATING | SUBSCRIBED  # Excludes those explicitly not involved.
    ACTIVE = INVITED | PARTICIPATING | SUBSCRIBED  # Those explicitly involved.


class Member(Serializable):

    def __init__(self, user, status=Status.NOT_INVITED):
        self.__user = user
        self.status = status

    def __repr__(self):
        return f'<{self.__class__.__name__} user={self.name} status={self.status} at {hex(id(self))}>'

    @property
    def name(self):
        return self.user.name

    @reference
    def user(self):
        return self.__user
