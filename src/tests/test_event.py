import os
import unittest
from bot.christmas_miracle_user import ChristmasMiracleUser
from plan.event import Event


class TestEvent(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = ChristmasMiracleUser('foo')

    def test_init_hierarchy(self):
        event_a = Event('a', self.user)
        event_b = Event('b', self.user, parent=event_a)

        self.assertFalse(event_a.parent)
        self.assertTrue(event_a.children)
        self.assertTrue(event_a.children[0] is event_b)

        self.assertFalse(event_b.children)
        self.assertTrue(event_b.parent)
        self.assertTrue(event_b.parent is event_a)

    def test_add_child(self):
        event_a = Event('a', self.user)
        event_b = Event('b', self.user)

        event_a.add_child(event_b)
        self.assertTrue(event_a.children)
        self.assertTrue(event_a.children[0] is event_b)
        self.assertTrue(event_b.parent)
        self.assertTrue(event_b.parent is event_a)

    def test_set_parent(self):
        event_a = Event('a', self.user)
        event_b = Event('b', self.user)

        event_b.parent = event_a
        self.assertTrue(event_b.parent)
        self.assertTrue(event_b.parent is event_a)
        self.assertTrue(event_a.children)
        self.assertTrue(event_a.children[0] is event_b)

    def test_reparent_tree(self):
        event_a = Event('a', self.user)
        event_b = Event('b', self.user)
        event_c = Event('c', self.user)
        event_d = Event('d', self.user)

        event_b.parent = event_a
        event_c.parent = event_b

        event_b.parent = event_d
        self.assertFalse(event_a.children)
        self.assertTrue(event_b.parent)
        self.assertTrue(event_b.parent is event_d)
        self.assertTrue(event_c.parent)
        self.assertTrue(event_c.parent is event_b)
        self.assertTrue(event_d.children)
        self.assertTrue(event_d.children[0] is event_b)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
