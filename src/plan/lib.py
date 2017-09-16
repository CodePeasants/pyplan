import asyncio
from fuzzywuzzy import process
import pytz
from pytz import timezone


def get_time_zone(time_zone=None, threshold=60):
    if time_zone is None:
        time_zone = 'UTC'

    result = process.extract(time_zone, pytz.all_timezones)
    if result[0][1] < threshold:
        raise ValueError('{time_zone} is an invalid time zone!'.format(**locals()))

    return timezone(result[0][0])


def get_event_loop():
    """
    Get's the current thread's event loop, whether running on the main thread or not
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop
