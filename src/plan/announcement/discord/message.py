from event.settings import EVERYONE
from event.announcement import Announcement
from event import lib


class Message(Announcement):

    def formatted(self):
        return ('__**{0.title}**__\n'
                '{0.message}').format(self)

    def send(self):
        members = self.get_members()
        if EVERYONE in members:
            targets = '@{}'.format(EVERYONE)
        else:
            targets = '@{}'.format(' '.join(['@{}'.format(x.user.discord_name) for x in self.get_members()]))

        loop = lib.get_event_loop()
        loop.run_until_complete(self.bot.say('{}\n{}'.format(targets, self.formatted())))
        loop.close()
