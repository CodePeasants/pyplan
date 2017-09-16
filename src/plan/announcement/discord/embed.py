from event.announcement.discord.abstract import AbstractDiscordAnnouncement
from event import lib


class Embed(AbstractDiscordAnnouncement):

    def formatted(self, color=None):
        pass  # todo return a discord Embed object.

    def send(self):
        loop = lib.get_event_loop()
        # todo get this to send to a specific text channel (e.g. announcements).
        loop.run_until_complete(self.bot.say(self.get_targets(), embed=self.formatted()))
        loop.close()
