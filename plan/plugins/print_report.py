# Package
from plan.report import Report
from plan.plugin_registry import RegisterMeta


class PrintReport(Report, metaclass=RegisterMeta):

    def render(self):
        return f'message: {self.message}'

    def get_targets(self):
        """This report has no targets. It will use the python built-in print method to send."""
        pass

    def send(self):
        print(self.render())
