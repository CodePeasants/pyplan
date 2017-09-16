import unittest
from plan.user import User
from plan.manager import Manager
from plan.event import Event


class TestManager(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestManager, self).__init__(*args, **kwargs)
        self.user = User('foo')

    def tearDown(self):
        super().tearDown()
        Manager().clear()

    def test_add(self):
        manager = Manager()
        event = Event('a', self.user)

        self.assertFalse(manager.events)

        manager.add(event)
        self.assertTrue(manager.events)
        self.assertTrue(manager.events[0] is event)

    def test_remove(self):
        manager = Manager()
        event = Event('a', self.user)

        manager.add(event)
        self.assertTrue(manager.events)

        manager.remove(event)
        self.assertFalse(manager.events)

    def test_persistence(self):
        self.assertTrue(Manager() is Manager())
        event = Event('a', self.user)
        Manager().add(event)
        self.assertTrue(Manager().events)
        self.assertTrue(Manager().events[0] is event)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
