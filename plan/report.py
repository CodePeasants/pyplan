# Package
from plan.member import Status
from plan.serializable import Serializable


class Report(Serializable):

    def __init__(self, audience=Status.GENERAL, message=''):
        super().__init__()
        self.audience = audience
        self.message = message

    def render(self):
        return self.message
