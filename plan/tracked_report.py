# Python standard library.
import pickle
from enum import Enum
from enum import auto
import abc

from plan.serializable import Serializable
from plan.time_range import TimeRange
from plan.schedule import Schedule
from plan.abstract_report import AbstractReport


class State(Enum):
    UNSENT = auto()
    READY = auto()
    SENDING = auto()
    SENT = auto()


class TrackedReport(Serializable, metaclass=abc.ABCMeta):

    def __init__(self, report, state=State.UNSENT):
        super().__init__()
        self.report = report
        self.state = state

    @abc.abstractmethod
    def resolve_state(self):
        pass


class ScheduledReport(TrackedReport):

    def __init__(self, report, state=State.UNSENT, schedule=None, last_send=None):
        super().__init__(report, state)
        self.report = report
        self.schedule = schedule or Schedule.now()
        self.last_send = last_send

    def resolve_state(self):
        """
        Updates the state of this report and returns it. Used by the Reporter to check if the report is ready to be
        sent yet.
        """
        if self.state not in (State.UNSENT, State.SENT):
            return self.state

        current_time = TimeRange.now()
        for each_time in self.schedule.times:
            # If there was no previous send or this scheduled time is more recent than the last send, check against
            # current time to see if this report is ready to send.
            if self.last_send is None or (self.last_send is not None and each_time > self.last_send):
                # If this scheduled time is less recent than the current time, the report should be sent.
                if each_time <= current_time:
                    self.state = State.READY

        return self.state


class TriggerReport(TrackedReport):

    def __init__(self, report, state=State.UNSENT, trigger=None):
        """
        Report to be sent when a certain event/trigger happens. Must be careful about what kind of callable we pass in,
        so that it still works when we serailize/deserialize it.

        :param AbstractReport report:
            The report to be sent.
        :param func trigger:
            Callable that returns a boolean. This will be evaluated on each reporter tick. When it evaluates to True,
            the report will be sent.
        """
        super().__init__(report, state)
        self.trigger = trigger

    def resolve_state(self):
        if self.state not in (State.UNSENT):
            return self.state

        if self.trigger is not None and self.trigger():
            self.state = State.READY
        return self.state

    @classmethod
    def from_dict(cls, data):
        obj_id = data.pop(ID_KEY)
        trigger = pickle.loads(data['trigger'])
        report_dict = data.get('report')
        report_cls = AbstractReport.get_type(report_dict)

        result = cls(report_cls.from_dict(report_dict), trigger)
        result.id = obj_id
