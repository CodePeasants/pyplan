# Python
import unittest

# Package
from plan.user import User
from plan.event import Event
from plan.report.print_report import PrintReport


class TestReport(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.owner = User('foo')
        self.event = Event('foo', self.owner)

    def test_print_report(self):
        report = PrintReport(self.event, title='title', message='message')
        expected_result = ('title: title\n'
                           'message:\n'
                           'message')
        self.assertEqual(expected_result, report.formatted())

    def test_get_members(self):
        pass


def main():
    unittest.main()


if __name__ == '__main__':
    main()
