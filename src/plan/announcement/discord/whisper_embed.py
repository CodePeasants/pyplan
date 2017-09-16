from event.announcement.discord.embed import Embed
from event import lib


class WhisperEmbed(Embed):

    def send(self):
        loop = lib.get_event_loop()
        # todo get bot to send this to target users.
        loop.run_until_complete(self.bot.whisper(self.get_targets(), embed=self.formatted()))
        loop.close()
