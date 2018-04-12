# Python standard lib
from datetime import datetime

# Package
from plan.serializable import Serializable
from plan.settings import TIME_ZONE


class TimeRange(Serializable):

    def __init__(self, start=None, end=None):
        if start is None:
            start = datetime.now(TIME_ZONE)

        if end is None:
            end = start

        if not all(isinstance(x, datetime) for x in [start, end]):
            raise TypeError('Must provide datetime objects!')

        if start > end:
            raise ValueError('Cannot have a start time greater than end time!')

        if not all(x.tzinfo for x in [start, end]):
            raise ValueError('datetime objects must have time zone info!')

        self.start = start
        self.end = end

    def __contains__(self, item):
        if isinstance(item, datetime):
            return self.start <= item <= self.end
        elif isinstance(item, self.__class__):
            return item.start >= self.start and item.end <= self.end
        else:
            raise TypeError('Invalid type!')

    def __eq__(self, other):
        if isinstance(other, datetime):
            return other == self.start and other == self.end
        elif isinstance(other, self.__class__):
            return other.start == self.start and other.end == self.end
        else:
            raise TypeError('Invalid type!')

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        if isinstance(other, self.__class__):
            return self.start > other.end
        elif isinstance(other, datetime):
            return self.start > other
        else:
            raise TypeError(f'Cannot compare {self.__class__.__name__} to {type(other)}.')

    def __ge__(self, other):
        if isinstance(other, self.__class__):
            return self.end <= other.start
        elif isinstance(other, datetime):
            return self.end <= other
        else:
            raise TypeError(f'Cannot compare {self.__class__.__name__} to {type(other)}.')

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.end < other.start
        elif isinstance(other, datetime):
            return self.end < other
        else:
            raise TypeError(f'Cannot compare {self.__class__.__name__} to {type(other)}.')

    def __le__(self, other):
        if isinstance(other, self.__class__):
            return self.end <= other.start
        elif isinstance(other, datetime):
            return self.end <= other
        else:
            raise TypeError(f'Cannot compare {self.__class__.__name__} to {type(other)}.')

    def astimezone(self, time_zone):
        start = self.start.astimezone(time_zone)
        end = self.end.astimezone(time_zone)
        return self.__class__(start, end)

    @classmethod
    def now(cls, time_zone=None):
        """Returns a TimeRange object for the current time."""
        current_time = datetime.now(time_zone)
        if not time_zone:
            current_time = TIME_ZONE.localize(current_time)
        return cls(current_time)
