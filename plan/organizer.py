from plan.member import Status
from logger import log


class Organizer:

    def __init__(self, event, potential_schedules=None, schedule=None, votes=None):
        self.__event = event
        self.__potential_schedules = potential_schedules or set()
        self.__schedule = schedule
        self.__votes = votes or {}

    def confirm_schedule(self, schedule=None):
        if schedule is None:
            self.__schedule = self.get_best_schedule()
        else:
            self.__schedule = schedule

    def unconfirm_schedule(self):
        self.__schedule = None

    @property
    def schedule(self):
        return self.__schedule

    @property
    def potential_schedules(self):
        return self.__potential_schedules

    @property
    def votes(self):
        return self.__votes

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
                'Schedule: {} is not among potential schedules: {}'.format(schedule, self.potential_schedules)
            )

        if member not in self.__event.registrar.members:
            raise PermissionError('{} is not a member of {}'.format(member, self.__event))

        if member.status not in [Status.INVITED, Status.PARTICIPATING]:
            raise PermissionError('{member} does not have permission to vote!'.format(**locals()))

        if member not in self.votes:
            self.votes[member] = set()
        self.votes[member].add(schedule)

    def add_potential_schedule(self, schedule):
        self.potential_schedules.add(schedule)

    def remove_potential_schedule(self, schedule):
        if schedule not in self.potential_schedules:
            log.warning('Schedule: {} not in potential schedules. Nothing to do.'.format(schedule))
            return

        # Check if any members have voted for the schedule being removed.
        voted_members = []
        for member in self.votes.keys():
            if schedule in self.votes[member]:
                voted_members.append(member)
                self.votes[member].remove(schedule)

        # todo do we want to notify members that a schedule they voted for was removed? Do we think they will care?
        self.potential_schedules.remove(schedule)
