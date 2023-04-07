from typing import Optional, Union

import discord
from discord.ext import commands

from pie import utils, check

class Vote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
            ctx.reply(emoji)
           
class VoteObject:
    pass
    

async def setup(bot) -> None:
    await bot.add_cog(Vote(bot))
