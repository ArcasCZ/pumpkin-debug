from typing import Optional, Union

import discord
from discord.ext import commands

from pie import utils, check

class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Commands

    @commands.guild_only()
    @check.acl2(check.ACLevel.SUBMOD)
    @commands.command(name="vote")
    async def vote(self, ctx, endTime: str, *, config: str):
        await ctx.reply(config)

async def setup(bot) -> None:
    await bot.add_cog(Debug(bot))
