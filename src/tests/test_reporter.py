# Python
import time
import unittest

# Package
from bot.christmas_miracle_user import ChristmasMiracleUser
from plan.reporter import Reporter
from plan.event import Event
from plan.announcement.print_announcement import PrintAnnouncement


class TestReporter(unittest.TestCase):

    def __init__(self):
        super().__init__()
        self.owner = ChristmasMiracleUser('foo')
        self.event = Event('foo', self.owner)
        self.reporter = Reporter()

    def setUp(self):
        super().setUp()
        self.reporter.reset()

    def test_tick(self):
        announcement = PrintAnnouncement(self.event, 'title', 'message')
        self.reporter.add_announcement(announcement)
        self.assertEqual(1, len(self.reporter.announcements))

        self.reporter.tick_rate = 0.1
        self.reporter.start()
        time.sleep(0.3)
        self.reporter.stop()

        self.assertFalse(self.reporter.announcements)

    # def test_tick_multiple(self):
    #     # todo add multiple times to the schedule. Verify that the announcement gets emitted at the appropriate times
    #     # and that it is removed only when the schedule completes.
    #     announcement = PrintAnnouncement(self.event, 'title', 'message')
    #     schedule = Schedule()
    #     schedule.add_time(TimeRange.relative())
    #
    #     self.reporter.add_announcement(announcement)
    #     self.assertEqual(1, len(self.reporter.announcements))
    #
    #     self.reporter.tick_rate = 0.1
    #     self.reporter.start()
    #     time.sleep(0.3)
    #     self.reporter.stop()
    #
    #     self.assertFalse(self.reporter.announcements)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
