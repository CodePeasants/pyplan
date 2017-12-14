# Python standard lib
from datetime import datetime
from pytz import timezone

# Package
from plan.serializable import Serializable
from plan.time_range import TimeRange
from plan.lib import get_time_zone
from logger import log


class Schedule(Serializable):

    def __init__(self, time_zone=None):
        super().__init__()
        self.__times = []
        self.__time_zone = time_zone or timezone('UTC')

    def __hash__(self):
        return hash('{}{}'.format(self.__time_zone, self.__times))

    def __repr__(self):
        return '<{0.__class__.__name__} time zone: {0.time_zone} times: {1} at {2}>'.format(
            self,
            len(self.times),
            hex(id(self))
        )

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return all(x in other.times for x in self.times) and self.time_zone == other.time_zone
        elif isinstance(other, datetime):
            return len(self.times) == 1 and self.times[0] == other
        else:
            raise TypeError(
                '{} cannot be compared against {} of type {}.'
                .format(self.__class__.__name__, other, type(other))
            )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            try:
                return min(self.times) < min(other.times)
            except ValueError:
                return False  # If either schedule has no times.
        elif isinstance(other, datetime):
            return len(self.times) == 1 and self.times[0] < other
        else:
            raise TypeError('Invalid type.')

    def __le__(self, other):
        if isinstance(other, self.__class__):
            try:
                return min(self.times) <= min(other.times)
            except ValueError:
                return False  # If either schedule has no times.
        elif isinstance(other, datetime):
            return len(self.times) == 1 and self.times[0] <= other
        else:
            raise TypeError('Invalid type.')

    def __gt__(self, other):
        if isinstance(other, self.__class__):
            try:
                return max(self.times) > max(other.times)
            except ValueError:
                return False  # If either schedule has no times.
        elif isinstance(other, datetime):
            return len(self.times) == 1 and self.times[0] > other
        else:
            raise TypeError('Invalid type.')

    def __ge__(self, other):
        if isinstance(other, self.__class__):
            try:
                return max(self.times) >= max(other.times)
            except ValueError:
                return False  # If either schedule has no times.
        elif isinstance(other, datetime):
            return len(self.times) == 1 and self.times[0] >= other
        else:
            raise TypeError('Invalid type.')

    @property
    def times(self):
        return [x.astimezone(self.time_zone) for x in self.__times]

    @property
    def time_zone(self):
        return self.__time_zone

    @time_zone.setter
    def time_zone(self, time_zone):
        self.__time_zone = get_time_zone(time_zone)

    @classmethod
    def now(cls):
        """Returns a Schedule object with only the current time added."""
        result = cls()
        result.add_time(TimeRange.now())
        return result

    def add_time(self, time):
        if not isinstance(time, TimeRange):
            raise ValueError('Invalid input! Must be TimeRange object!')

        converted = time.astimezone(self.time_zone)

        for time_range in self.times:
            if converted in time_range:
                log.warning('Given time: {} already included in scheduled times. Nothing to do.'.format(time_range))
                return

        self.times.append(time)

    def remove_time(self, time_range):
        if time_range in self.times:
            self.times.remove(time_range)
