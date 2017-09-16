# 3ps
from fuzzywuzzy import process
import pytz
from pytz import timezone

# Package
from plan.settings import TIME_ZONE


class Singleton(type):
    """To be used as a metaclass."""

    __instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            cls.__instances[cls] = super().__call__(*args, **kwargs)
        return cls.__instances[cls]


def get_time_zone(time_zone=None, threshold=60):
    time_zone = time_zone or TIME_ZONE
    result = process.extract(time_zone, pytz.all_timezones)
    if result[0][1] < threshold:
        raise ValueError('{time_zone} is an invalid time zone!'.format(**locals()))

    return timezone(result[0][0])
