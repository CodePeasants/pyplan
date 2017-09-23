# Python standard library
import threading

# Package
from plan.ticker import Ticker
from plan.serializable import Serializable
from plan.tracked_report import State


_lock = threading.Lock()


class Reporter(Serializable):

    def __init__(self, tracked_reports=None):
        super().__init__()
        self.tracked_reports = tracked_reports or []
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

    def start(self):
        if not self.__ticker.is_alive():
            self.__ticker.start()

    def stop(self):
        if self.__ticker is not None and self.__ticker.is_alive():
            self.__ticker.stop()

    def _tick(self):
        """Checks & sends tracked reports if they are ready."""
        for tracked_report in self.tracked_reports:
            state = tracked_report.resolve_state
            if state == State.READY:
                tracked_report.state = State.SENDING
                with _lock:
                    tracked_report.report.send()
                tracked_report.state = State.SENT
