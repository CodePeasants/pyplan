from functools import partial
import unittest
from plan import lib


class TestLib(unittest.TestCase):

    def test_get_time_zone(self):
        tz = lib.get_time_zone('UTC', threshold=100)
        self.assertTrue(tz)

    def test_get_bad_time_zone(self):
        func = partial(lib.get_time_zone, 'foobar', threshold=100)
        self.assertRaises(ValueError, func)

    def test_get_time_zone_threshold(self):
        test_case = 'east'
        tz = lib.get_time_zone(test_case, threshold=30)
        self.assertTrue(tz)

        func = partial(lib.get_time_zone, test_case, threshold=100)
        self.assertRaises(ValueError, func)


if __name__ == '__main__':
    unittest.main()
