# Python standard library
from uuid import UUID

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


class abstract_classmethod(classmethod):

    __isabstractmethod__ = True

    def __init__(self, callable):
        callable.__isabstractmethod__ = True
        super(abstract_classmethod, self).__init__(callable)


def is_id_string(value):
    """Check if the provided string is a valid ID."""
    try:
        UUID(value, version=4)
    except (ValueError, AttributeError, TypeError):
        return False
    else:
        return True


def get_time_zone(time_zone=None, threshold=60):
    time_zone = time_zone or TIME_ZONE
    result = process.extract(time_zone, pytz.all_timezones)
    if result[0][1] < threshold:
        raise ValueError('{time_zone} is an invalid time zone!'.format(**locals()))

    return timezone(result[0][0])
