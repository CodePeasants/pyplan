# Python
import unittest

# Package
from bot.christmas_miracle_user import ChristmasMiracleUser
from event.event import Event
from event.announcement.print_announcement import PrintAnnouncement


class TestAnnouncement(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.owner = ChristmasMiracleUser('foo')
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
