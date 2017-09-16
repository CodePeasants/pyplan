# Python
import threading

# Package
from lib import Singleton
from plan.ticker import Ticker
from plan.schedule import Schedule
from plan.time_range import TimeRange


__lock = threading.Lock()


class Reporter(metaclass=Singleton):

    def __init__(self, announcements=None):
        self.__announcements = announcements or []
        self.__ticker = Ticker()
        self.__ticker.add_callback(self._tick)

    @property
    def is_alive(self):
        return self.__ticker.is_alive()

    @property
    def tick_rate(self):
        return self.__ticker.tick_rate

    @tick_rate.setter
    def tick_rate(self, value):
        self.__ticker.tick_rate = value

    def reset(self):
        self.stop()
        self.__announcements = []
        self.__ticker = Ticker()
        self.__ticker.add_callback(self._tick)
        self.start()

    def start(self):
        if not self.__ticker.is_alive():
            self.__ticker.start()

    def stop(self):
        if self.__ticker is not None and self.__ticket.is_alive():
            self.__ticker.stop()

    def _tick(self):
        """Checks scheduled announcements against the current time & announces."""
        current_time = TimeRange.now()
        for scheduled_announcement in self.scheduled_announcements[:]:
            # Collect all of the times from the schedule earlier than the current time.
            remove_times = []
            for each_time in scheduled_announcement.schedule.times[:]:
                if each_time <= current_time:
                    remove_times.append(each_time)

            # If there are any old times, remove them from the schedule and send the announcement.
            if remove_times:
                with __lock:
                    for old_time in remove_times:
                        scheduled_announcement.schedule.remove_time(old_time)
                scheduled_announcement.announcement.send()

            # If there are no more scheduled times for the announcement, delete it.
            if not scheduled_announcement.schedule.times:
                with __lock:
                    self.scheduled_announcements.remove(scheduled_announcement)

    @property
    def scheduled_announcements(self):
        return self.__announcements

    def add_announcement(self, announcement, schedule=None):
        if not isinstance(announcement, ScheduledAnnouncement):
            announcement = ScheduledAnnouncement(announcement, schedule)
        if announcement not in self.announcements:
            self.announcements.append(announcement)

    def remove_announcement(self, announcement):
        if announcement in self.announcements:
            self.announcements.remove(announcement)


class ScheduledAnnouncement:

    def __init__(self, announcement, schedule=None):
        self.announcement = announcement
        self.schedule = schedule or Schedule.now()
