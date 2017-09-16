# Python
import unittest

# Package
from plan.user import User
from plan.event import Event
from plan.announcement.print_announcement import PrintAnnouncement


class TestAnnouncement(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.owner = User('foo')
        self.event = Event('foo', self.owner)

    def test_print_announcement(self):
        announcement = PrintAnnouncement(self.event, title='title', message='message')
        expected_result = ('to: foo\n'
                           'title: title\n'
                           'message:\n'
                           'message')
        self.assertEqual(expected_result, announcement.formatted())

    def test_get_members(self):
        pass


def main():
    unittest.main()


if __name__ == '__main__':
    main()
