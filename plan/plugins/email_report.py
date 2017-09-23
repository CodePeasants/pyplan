from plan.abstract_report import AbstractReport
from plan.plugin_registry import RegisterMeta


class EmailReport(AbstractReport, metaclass=RegisterMeta):

    def format(self):
        pass  # todo
