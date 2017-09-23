import unittest
from plan.user import User
from plan.member import Status
from plan.registry import Registry


class TestRegistry(unittest.TestCase):

    def setUp(self):
        super(TestRegistry, self).setUp()
        self.user = User('foo')

    def test_register(self):
        reg = Registry()
        self.assertFalse(reg.members)

        reg.register(self.user, Status.INVITED)
        self.assertEqual(1, len(reg.members))
        self.assertEqual(self.user, reg.members[0].user)
        self.assertEqual(Status.INVITED, reg.members[0].status)

    def test_register_status_change(self):
        reg = Registry()
        reg.register(self.user, Status.INVITED)
        self.assertEqual(Status.INVITED, reg.members[0].status)

        reg.register(self.user, Status.SUBSCRIBED)
        self.assertEqual(1, len(reg.members))
        self.assertEqual(self.user, reg.members[0].user)
        self.assertEqual(Status.SUBSCRIBED, reg.members[0].status)

    def test_de_register(self):
        reg = Registry()
        reg.register(self.user, Status.INVITED)
        self.assertEqual(1, len(reg.members))

        reg.de_register(self.user)
        self.assertEqual(0, len(reg.members))

    def test_get(self):
        reg = Registry()
        reg.register(self.user, Status.INVITED)

        self.assertFalse(reg.get(status=Status.SUBSCRIBED))
        self.assertTrue(reg.get(status=Status.INVITED))

    def test_requirement(self):
        reg = Registry(requirement=2)
        reg.register(self.user, Status.INVITED)
        self.assertFalse(reg.requirement_met)

        # Requirement still not met, because the one registered member is merely invited, not participating.
        reg.requirement = 1
        self.assertFalse(reg.requirement_met)

        reg.register(self.user, Status.PARTICIPATING)
        self.assertTrue(reg.requirement_met)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
