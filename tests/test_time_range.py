# Python standard lib
import time
import unittest
from datetime import datetime

# 3ps
import pytz

# Package
from plan.time_range import TimeRange


class TestTimeRange(unittest.TestCase):

    def test_init(self):
        foo = TimeRange()
        self.assertEqual(foo.start, foo.end)

    def test_contains(self):
        foo = TimeRange(datetime(2015, 1, 1, tzinfo=pytz.UTC), datetime(2016, 1, 1, tzinfo=pytz.UTC))
        self.assertIn(datetime(2015, 5, 1, tzinfo=pytz.UTC), foo)
        self.assertNotIn(datetime(2017, 1, 1, tzinfo=pytz.UTC), foo)
        self.assertIn(datetime(2015, 1, 1, tzinfo=pytz.UTC), foo)
        self.assertNotIn(datetime(2017, 1, 1, tzinfo=pytz.UTC), foo)

    def test_eq(self):
        foo = TimeRange(datetime(2015, 1, 1, tzinfo=pytz.UTC), datetime(2016, 1, 1, tzinfo=pytz.UTC))
        self.assertEqual(TimeRange(datetime(2015, 1, 1, tzinfo=pytz.UTC), datetime(2016, 1, 1, tzinfo=pytz.UTC)), foo)
        self.assertNotEqual(TimeRange(datetime(2015, 1, 1, tzinfo=pytz.UTC), datetime(2016, 1, 2, tzinfo=pytz.UTC)), foo)

    def test_astimezone(self):
        foo = TimeRange(datetime(2015, 10, 1, 10, 30, tzinfo=pytz.UTC), datetime(2016, 10, 1, 15, 30, tzinfo=pytz.UTC))
        bar = foo.astimezone(pytz.timezone('US/Eastern'))

        eastern_start = datetime(2015, 10, 1, 6, 30, tzinfo=pytz.timezone('US/Eastern'))
        eastern_end = datetime(2015, 10, 1, 11, 30, tzinfo=pytz.timezone('US/Eastern'))

        self.assertEqual(eastern_start.hour, bar.start.hour)
        self.assertEqual(eastern_end.hour, bar.end.hour)

    def test_now(self):
        foo = TimeRange.now(pytz.UTC)
        time.sleep(0.5)
        dt = datetime.now(pytz.UTC)
        self.assertGreater(dt, foo)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
