# Package
from plan.report.abstract_report import AbstractReport


class PrintReport(AbstractReport):

    def formatted(self):
        return ('title: {0.title}\n'
                'message:\n'
                '{0.message}').format(self)

    def get_targets(self):
        """This report has no targets. It will use the python built-in print method to send."""
        pass

    def send(self):
        print(self.formatted())
