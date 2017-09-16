import os
from functools import partial
import unittest
from bot.christmas_miracle_user import ChristmasMiracleUser
from event.event import Event
from event.organizer import Organizer
from event.schedule import Schedule
from event.time_range import TimeRange
from event.member import Status


class TestOrganizer(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestOrganizer, self).__init__(*args, **kwargs)
        self.owner = ChristmasMiracleUser('foo')
        self.invited_user = ChristmasMiracleUser('bar')
        self.uninvited_user = ChristmasMiracleUser('foobar')

        self.event = Event('a', self.owner)
        self.invited_member = self.event.registrar.register(self.invited_user)
        self.uninvited_member = self.event.registrar.register(self.uninvited_user, Status.NOT_INVITED)

    def test_init(self):
        org = Organizer(self.event)
        self.assertFalse(org.votes)
        self.assertFalse(org.potential_schedules)

    def test_add_potential_schedule(self):
        org = Organizer(self.event)
        schedule = Schedule()

        org.add_potential_schedule(schedule)
        self.assertEqual([schedule], list(org.potential_schedules))

    def test_remove_potential_schedule(self):
        org = Organizer(self.event, [Schedule()])
        org.remove_potential_schedule(org.potential_schedules[0])
        self.assertFalse(org.potential_schedules)

    def test_vote(self):
        schedule_a = Schedule()
        schedule_b = Schedule()

        schedule_a.add_time(TimeRange.now())
        schedule_b.add_time(TimeRange.now())

        org = Organizer(self.event, [schedule_a, schedule_b])
        org.vote(self.invited_member, schedule_b)

        self.assertEqual({self.invited_member: set([schedule_b])}, org.votes)

    def test_vote_multiple(self):
        schedule_a = Schedule()
        schedule_b = Schedule()

        schedule_a.add_time(TimeRange.now())
        schedule_b.add_time(TimeRange.now())

        org = Organizer(self.event, [schedule_a, schedule_b])
        org.vote(self.invited_member, schedule_b)
        org.vote(self.invited_member, schedule_b)

        self.assertEqual({self.invited_member: set([schedule_b])}, org.votes)

    def test_vote_change(self):
        schedule_a = Schedule()
        schedule_b = Schedule()

        schedule_a.add_time(TimeRange.now())
        schedule_b.add_time(TimeRange.now())

        org = Organizer(self.event, [schedule_a, schedule_b])
        org.vote(self.invited_member, schedule_b)
        org.vote(self.invited_member, schedule_a)

        self.assertEqual({self.invited_member: set([schedule_a])}, org.votes)

    def test_vote_invalid_member(self):
        schedule_a = Schedule()
        schedule_b = Schedule()

        schedule_a.add_time(TimeRange.now())
        schedule_b.add_time(TimeRange.now())

        org = Organizer(self.event, [schedule_a, schedule_b])

        func = partial(org.vote, self.uninvited_member, schedule_a)
        self.assertRaises(PermissionError, func)
        self.assertEqual({}, org.votes)

    def test_get_best_schedule(self):
        schedule_a = Schedule()
        schedule_b = Schedule()

        schedule_a.add_time(TimeRange.now())
        schedule_b.add_time(TimeRange.now())

        org = Organizer(self.event, [schedule_a, schedule_b])
        org.vote(self.invited_member, schedule_b)

        self.assertEqual(schedule_b, org.get_best_schedule())

    def test_confirm_schedule(self):
        schedule_a = Schedule()
        org = Organizer(self.event, [schedule_a])
        self.assertEqual(None, org.schedule)

        org.confirm_schedule(schedule_a)
        self.assertEqual(schedule_a, org.schedule)

    def test_unconfirm_schedule(self):
        schedule_a = Schedule()
        org = Organizer(self.event, [schedule_a])
        org.confirm_schedule(schedule_a)
        org.unconfirm_schedule()
        self.assertEqual(None, org.schedule)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
