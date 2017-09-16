from event.announcement.discord.abstract import AbstractDiscordAnnouncement
from event import lib


class WhisperMessage(AbstractDiscordAnnouncement):

    def send(self):
        loop = lib.get_event_loop()
        # todo get bot to send this to target users.
        loop.run_until_complete(self.bot.whisper('{}\n{}'.format(self.get_targets(), self.formatted())))
        loop.close()
    
