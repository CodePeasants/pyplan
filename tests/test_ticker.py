# Python
from io import StringIO
import time
import unittest

# Package
from plan.ticker import Ticker


class TestTicker(unittest.TestCase):

    def foo(self):
        self.stream.write("1")

    def setUp(self):
        super().setUp()
        self.ticker = Ticker()
        self.stream = StringIO()

    def test_add_callback(self):
        self.assertFalse(self.ticker.callbacks)
        self.ticker.add_callback(self.foo)
        self.assertEqual(1, len(self.ticker.callbacks))
        self.assertEqual(self.foo, self.ticker.callbacks[0])

    def test_add_callback_multiple(self):
        self.assertFalse(self.ticker.callbacks)
        self.ticker.add_callback(self.foo)
        self.ticker.add_callback(self.foo)
        self.ticker.add_callback(self.foo)
        self.assertEqual(1, len(self.ticker.callbacks))
        self.assertEqual(self.foo, self.ticker.callbacks[0])

    def test_remove_callback(self):
        self.assertFalse(self.ticker.callbacks)
        self.ticker.add_callback(self.foo)
        self.assertTrue(self.ticker.callbacks)
        self.ticker.remove_callback(self.foo)
        self.assertFalse(self.ticker.callbacks)

    def test_remove_callback_multiple(self):
        self.assertFalse(self.ticker.callbacks)
        self.ticker.add_callback(self.foo)
        self.assertTrue(self.ticker.callbacks)
        self.ticker.remove_callback(self.foo)
        self.ticker.remove_callback(self.foo)
        self.ticker.remove_callback(self.foo)
        self.assertFalse(self.ticker.callbacks)

    def test_callback(self):
        self.ticker.add_callback(self.foo)
        self.assertFalse(self.ticker.is_alive())

        self.ticker.tick_rate = 0.3
        self.ticker.start()
        self.assertTrue(self.ticker.is_alive())

        time.sleep(0.4)

        self.ticker.stop()
        self.stream.seek(0)
        self.assertEqual('11', self.stream.read())

        # Note: We do not kill the thread itself. Instead, we stop the work it is doing.
        self.assertFalse(self.ticker.is_ticking)
        self.assertTrue(self.ticker.is_alive())


def main():
    unittest.main()


if __name__ == '__main__':
    main()
