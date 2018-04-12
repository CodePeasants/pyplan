# Python standard library
import weakref

# Package
from plan.serializable import Serializable
from plan.serializable import reference
from plan.serializable import weak_reference
from plan.member import Status
from plan.logger import log


class Organizer(Serializable):

    def __init__(self, event, potential_schedules=None, schedule=None, votes=None):
        super().__init__()
        self.__event = None
        self.__potential_schedules = set()
        self.__schedule = None
        self.__votes = {}

        if event is not None:
            self.event = event

        if potential_schedules is not None:
            self.potential_schedules = potential_schedules

        if schedule is not None:
            self.schedule = schedule

        if votes is not None:
            self.__votes = votes

    @weak_reference
    def event(self):
        return self.__event

    @event.setter
    def event(self, value):
        try:
            self.__event = weakref.proxy(value)
        except TypeError:
            self.__event = value

    @reference
    def schedule(self):
        return self.__schedule

    @schedule.setter
    def schedule(self, value):
        self.__schedule = value

    @reference
    def potential_schedules(self):
        return self.__potential_schedules

    @potential_schedules.setter
    def potential_schedules(self, value):
        self.__potential_schedules = value

    @reference
    def votes(self):
        return self.__votes

    @votes.setter
    def votes(self, value):
        self.__votes = value

    def confirm_schedule(self, schedule=None):
        if schedule is None:
            self.__schedule = self.get_best_schedule()
        else:
            self.__schedule = schedule

    def unconfirm_schedule(self):
        self.__schedule = None

    def get_best_schedule(self):
        """Pick the most popular, earliest schedule."""
        # Tally up the votes.
        vote_counts = dict((x, 0) for x in self.potential_schedules)
        for votes in self.votes.values():
            for schedule in votes:
                vote_counts[schedule] += 1

        # Determine all of the schedules with the most votes.
        winning_value = max(vote_counts.values())
        winners = [k for k, v in vote_counts.items() if v == winning_value]

        # Pick among the winners the earliest occurring schedule.
        return min(winners)

    def vote(self, member, schedule):
        if schedule not in self.potential_schedules:
            raise ValueError(
                f'Schedule: {schedule} is not among potential schedules: {self.potential_schedules}'
            )

        if member not in self.__event.registry.members:
            raise PermissionError(f'{member} is not a member of {self.__event}')

        if member.status not in [Status.INVITED, Status.PARTICIPATING]:
            raise PermissionError(f'{member} does not have permission to vote!')

        if member not in self.votes:
            self.votes[member] = set()
        self.votes[member].add(schedule)

    def add_potential_schedule(self, schedule):
        self.potential_schedules.add(schedule)

    def remove_potential_schedule(self, schedule):
        if schedule not in self.potential_schedules:
            log.warning(f'Schedule: {schedule} not in potential schedules. Nothing to do.')
            return

        # Check if any members have voted for the schedule being removed.
        voted_members = []
        for member in self.votes.keys():
            if schedule in self.votes[member]:
                voted_members.append(member)
                self.votes[member].remove(schedule)

        # todo do we want to notify members that a schedule they voted for was removed? Do we think they will care?
        self.potential_schedules.remove(schedule)
