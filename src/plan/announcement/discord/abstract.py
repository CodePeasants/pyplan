# Python
import abc

# Package
from event.announcement import Announcement
from event.settings import EVERYONE


class AbstractDiscordAnnouncement(Announcement, metaclass=abc.ABCMeta):

    def get_targets(self):
        members = self.get_members()
        if EVERYONE in members:
            targets = '@{}'.format(EVERYONE)
        else:
            targets = '@{}'.format(' '.join(['@{}'.format(x.user.discord_name) for x in self.get_members()]))

        return targets
