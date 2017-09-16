# Python
import time
import unittest

# Package
from plan.user import User
from plan.reporter import Reporter
from plan.event import Event
from plan.report.print_report import PrintReport


class TestReporter(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.owner = User('foo')
        self.event = Event('foo', self.owner)
        self.reporter = Reporter()

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.reporter.reset()

    def test_tick(self):
        report = PrintReport(self.event, 'title', 'message')
        self.reporter.add_report(report)
        self.assertEqual(1, len(self.reporter.reports))

        self.reporter.tick_rate = 0.1
        self.reporter.start()
        time.sleep(0.2)
        self.reporter.stop()

        self.assertFalse(self.reporter.reports)

    # def test_tick_multiple(self):
    #     # todo add multiple times to the schedule. Verify that the report gets emitted at the appropriate times
    #     # and that it is removed only when the schedule completes.
    #     report = PrintReport(self.event, 'title', 'message')
    #     schedule = Schedule()
    #     schedule.add_time(TimeRange.relative())
    #
    #     self.reporter.add_report(report)
    #     self.assertEqual(1, len(self.reporter.reports))
    #
    #     self.reporter.tick_rate = 0.1
    #     self.reporter.start()
    #     time.sleep(0.3)
    #     self.reporter.stop()
    #
    #     self.assertFalse(self.reporter.reports)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
