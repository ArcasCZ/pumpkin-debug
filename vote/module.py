import emojis
import re

from typing import Optional, Union

import discord
from discord.ext import commands

from pie import utils, check

EMOJI_REGEX = "^<[a-zA-Z0-9]*:[a-zA-Z0-9]+:[0-9]+>$"

class Vote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    # Helper functions
    
    @staticmethod
    def check_emoji(
        bot: discord.Client,
        emoji: str,
    ) -> bool:
        """Verifies if the str is valid emoji or not.
        Args:
            bot: :class:`discord.Client` used to search for Emoji
            emoji: string to check
        Returns:
            True if it's known emoji
        """
        
        if emojis.count(emoji) == 1:
            return True
        
        if re.match(EMOJI_REGEX, emoji):
            found_emoji = discord.utils.get(bot.emojis, name=emoji.split(":")[1])
            if not found_emoji:
                return False
            return True
        
        

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
            await ctx.reply(Vote.check_emoji(emoji))
            
            

           
class VoteObject:
    pass
    

async def setup(bot) -> None:
    await bot.add_cog(Vote(bot))
