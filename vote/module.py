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
    async def vote(self, ctx, datetime_str: str, *, config: str):
        try:
            end_time = utils.time.parse_datetime(datetime_str)
        except dateutil.parser.ParserError:
            await ctx.reply(
                _(
                    ctx,
                    "I don't know how to parse `{datetime_str}`, please try again.",
                ).format(datetime_str=datetime_str)
            )
            return
        
        await ctx.reply(end_time)
           
class VoteObject:
    pass
    

async def setup(bot) -> None:
    await bot.add_cog(Vote(bot))
