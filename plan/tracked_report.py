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

    def __init__(self, report=None, state=State.UNSENT):
        super().__init__()
        self.report = report
        self.state = state

    @abc.abstractmethod
    def resolve_state(self):
        pass

    def to_dict(self):
        result = super().to_dict()
        result['report'] = self.report.to_dict()
        result['state'] = self.state.value
        return result

    def from_dict(cls, data):
        result = super().from_dict(data)
        result.state = State(data.get('state'))

        report_dict = data.get('report')
        report_cls = AbstractReport.get_type(report_dict)
        report = report_cls.from_dict(report_dict)
        result.report = report
        return result


class ScheduledReport(TrackedReport):

    def __init__(self, report=None, state=State.UNSENT, schedule=None, last_send=None):
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

    def to_dict(self):
        result = super().to_dict()
        result['schedule'] = self.schedule.to_dict()
        result['last_send'] = self.last_send
        return result


class TriggerReport(TrackedReport):

    def __init__(self, report=None, state=State.UNSENT, trigger=None):
        """
        Report to be sent when a certain event/trigger happens. Must be careful about what kind of callable we pass in,
        so that it still works when we serailize/deserialize it.

        Here is an example of how you can make a safe trigger. In this case, we want a report to be sent when a
        particular event's status changes to SCHEDULED, meaning a scheduled time has been decided upon:

        >>> from plan.object_registry import ObjectRegistry
        >>> trigger = lambda : ObjectRegistry.get(event.id).status == Status.SCHEDULED

        Because we use the object registry to get the event by it's ID, this trigger will survive
        serialization & deserialization.

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

    def to_dict(self):
        result = super().to_dict()
        result['trigger'] = pickle.dumps(self.trigger)
        return result

    @classmethod
    def from_dict(cls, data):
        result = super().from_dict(data)
        result.trigger = pickle.loads(data.get('trigger'))
        return result
