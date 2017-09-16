# Python
import threading

# Package
from lib import Singleton
from plan.ticker import Ticker
from plan.schedule import Schedule
from plan.time_range import TimeRange


__lock = threading.Lock()


class Reporter(metaclass=Singleton):

    def __init__(self, reports=None):
        self.__reports = reports or []
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
        self.__reports = []
        self.__ticker = Ticker()
        self.__ticker.add_callback(self._tick)
        self.start()

    def start(self):
        if not self.__ticker.is_alive():
            self.__ticker.start()

    def stop(self):
        if self.__ticker is not None and self.__ticker.is_alive():
            self.__ticker.stop()

    def _tick(self):
        """Checks scheduled reports against the current time & announces."""
        current_time = TimeRange.now()
        for scheduled_report in self.scheduled_reports[:]:
            # Collect all of the times from the schedule earlier than the current time.
            remove_times = []
            for each_time in scheduled_report.schedule.times[:]:
                if each_time <= current_time:
                    remove_times.append(each_time)

            # If there are any old times, remove them from the schedule and send the report.
            if remove_times:
                with __lock:
                    for old_time in remove_times:
                        scheduled_report.schedule.remove_time(old_time)
                scheduled_report.report.send()

            # If there are no more scheduled times for the report, delete it.
            if not scheduled_report.schedule.times:
                with __lock:
                    self.scheduled_reports.remove(scheduled_report)

    @property
    def scheduled_reports(self):
        return self.__reports

    def add_report(self, report, schedule=None):
        if not isinstance(report, ScheduledReport):
            report = ScheduledReport(report, schedule)
        if report not in self.reports:
            self.reports.append(report)

    def remove_report(self, report):
        if report in self.reports:
            self.reports.remove(report)


class ScheduledReport:

    def __init__(self, report, schedule=None):
        self.report = report
        self.schedule = schedule or Schedule.now()
