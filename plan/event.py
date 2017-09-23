from enum import Enum
from enum import auto
from plan.organizer import Organizer
from plan.registry import Registry
from plan.lib import get_time_zone


class Status(Enum):
    SCHEDULING = auto()
    SCHEDULED = auto()
    IN_PROGRESS = auto()
    COMPLETE = auto()
    ABANDONED = auto()


class Event:

    def __init__(self, name, owner=None, status=Status.SCHEDULING, required_participants=None, registration_cutoff=None,
                 time_zone=None, auto_confirm_schedule=True, parent=None):
        """
        :param str name:
            Name of the event.
        :param AbstractUser owner:
            User that owns the event.
        :param Status status:
            Initial status of the event.
        :param None|int required_participants:
            Optionally specify that this event has a minimum required number of participants to finish scheduling.
        :param None|TimeRange registration_cutoff:
            Optionally specify a cutoff time for registration.
        :param timezone time_zone:
            The timezone the event will use when internally tracking times.
        :param bool auto_confirm_schedule:
            If a cutoff time was specified and the requirements are met at that time, automatically flips the event
            status to scheduled.
        :param None|Event parent:
            Optionally specify a parent event that this is part of.
        """
        self.name = name
        self.owner = owner
        self.organizer = Organizer(self)
        self.registry = Registry(required_participants)
        self.registration_cutoff = registration_cutoff
        self.auto_confirm_schedule = auto_confirm_schedule
        self.status = status
        self.time_zone = get_time_zone(time_zone)

        self.__parent = None
        self.__children = []

        if parent is not None:
            self.parent = parent

    @property
    def parent(self):
        return self.__parent

    @parent.setter
    def parent(self, value):
        if isinstance(value, self.__class__):
            if self.parent is value:
                return

            if self.parent is not None:
                self.parent.remove_child(self)

            self.__parent = value
            value.add_child(self)
        elif value is None:
            if self.parent is not None:
                self.parent.remove_child(self)
            else:
                self.__parent = None
        else:
            raise TypeError('Cannot parent Event to: {} of type: {}'.format(value, type(value)))

    @property
    def children(self):
        return self.__children

    def add_child(self, event):
        if event is self:
            raise RuntimeError('Cannot parent an event to itself!')

        if event.parent != self:
            event.parent = self
        elif event not in self.children:
            self.children.append(event)

    def remove_child(self, event):
        if event in self.children:
            self.children.remove(event)
            event.parent = None
