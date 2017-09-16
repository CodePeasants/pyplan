from cogs.base_cog import BaseCog
from discord.ext import commands
from event import settings


class Event(BaseCog):

    def __init__(self, bot):
        super().__init__(bot, settings.EVENT_SAVE)

    @commands.command(pass_context=True)
    async def event(self, ctx, *args):
        """
        """
        await self.bot.say('foobar')
