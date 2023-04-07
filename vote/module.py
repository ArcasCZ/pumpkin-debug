import re

from typing import Optional, Union

import discord
from discord.ext import commands

from pie import utils, check

EMOJI_REGEX = "^:[a-zA-Z0-9]+:$"

class Vote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    # Helper functions
    
    @staticmethod
    def emoji_decode(
        bot: discord.Client,
        emoji: str,
    ) -> Optional[Union[str, discord.Emoji, discord.PartialEmoji]]:
        """If emoji is ID, it tries to look it up in bot's emoji DB.
        Otherwise it returns the emoji untouched as string.
        Args:
            bot: :class:`discord.Client` used to search for Emoji
            emoji: UTF-8 emoji or emoji's ID
        Returns:
            UTF-8 emoji or Discord Emoji
        """
        
        if re.match(EMOJI_REGEX, emoji):
            found_emoji = discord.utils.get(bot.emojis, name=emoji.replace(":", ""))
            if not found_emoji:
                return None
            return str(found_emoji.id)
        else:
            return emoji
        
        if emoji is None:
            return None

        if not emoji.isdigit():
            return emoji

        found_emoji = discord.utils.get(bot.emojis, id=int(emoji))
        if found_emoji:
            return found_emoji
        else:
            return emoji

    # Commands

    @commands.guild_only()
    @check.acl2(check.ACLevel.SUBMOD)
    @commands.command(name="vote")
    async def vote(self, ctx, endtime_str: str, *, config: str):
        try:
            end_time = utils.time.parse_datetime(endtime_str)
        except dateutil.parser.ParserError:
            await ctx.reply(
                _(
                    ctx,
                    "I don't know how to parse `{endtime_str}`, please try again.",
                ).format(endtime_str=endtime_str)
            )
            return
        
        for line in config.splitlines():
            (emoji, description) = line.split(maxsplit=1)
            #await ctx.reply("`{emoji}`".format(emoji=emoji.__class__))
            await ctx.reply(discord.utils.get(self.bot.emojis, name=emoji))
            

           
class VoteObject:
    pass
    

async def setup(bot) -> None:
    await bot.add_cog(Vote(bot))
