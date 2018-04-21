from plan.report import Report
from plan.plugin_registry import RegisterMeta


class EmailReport(Report, metaclass=RegisterMeta):

    def render(self):
        pass  # todo
