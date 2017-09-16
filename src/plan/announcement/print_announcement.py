from plan.announcement import Announcement
from plan.settings import EVERYONE


class PrintAnnouncement(Announcement):

    def formatted(self):
        return ('to: {1}\n'
                'title: {0.title}\n'
                'message:\n'
                '{0.message}').format(self, self.get_targets())

    def get_targets(self):
        members = self.get_members()
        targets = [x.user.name for x in members if hasattr(x, 'user')]
        if EVERYONE in members:
            targets.insert(0, EVERYONE)
        return targets

    def send(self):
        print(self.formatted())
