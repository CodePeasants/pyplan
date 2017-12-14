# Python standard lib
from datetime import datetime
from pytz import timezone

# Package
from plan.serializable import Serializable


class TimeRange(Serializable):

    def __init__(self, start, end=None):
        if end is None:
            end = start

        if start > end:
            raise ValueError('Cannot have a start time greater than end time!')

        if not all(isinstance(x, datetime) for x in [start, end]):
            raise TypeError('Must provide datetime objects!')

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

    def astimezone(self, time_zone):
        start = self.start.astimezone(time_zone)
        end = self.end.astimezone(time_zone)
        return self.__class__(start, end)

    @classmethod
    def now(cls):
        """Returns a TimeRange object for the current time."""
        current_time = datetime.now()
        current_time = timezone('UTC').localize(current_time)
        return cls(current_time)
