import emoji
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
    
    def check_emoji(
        self,
        emoji_str: str,
    ) -> bool:
        """Verifies if the str is valid emoji or not.
        Args:
            emoji_str: string to check
        Returns:
            True if it's known emoji
        """
        
        if emoji.is_emoji(emoji_str):
            return True
        
        if re.match(EMOJI_REGEX, emoji_str):
            found_emoji = discord.utils.get(self.bot.emojis, name=emoji_str.split(":")[1])
            if not found_emoji:
                return False
            return True
            
        return False
        
        

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
            await ctx.reply(self.check_emoji(emoji))
            
            

           
class VoteObject:
    pass
    

async def setup(bot) -> None:
    await bot.add_cog(Vote(bot))
