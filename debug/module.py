import datetime
import random
from typing import Optional, Union, Dict, List

import discord
from discord.ext import commands, tasks

from core import utils, check


LIMITS_MESSAGE = [15, 25]
LIMITS_REACTION = [0, 5]

TIMER_MESSAGE = 60
TIMER_REACTION = 30


class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Commands

    @commands.guild_only()
    @commands.group(name="debug")
    @commands.check(check.acl)
    async def debug_(self, ctx):
        """Debug tools"""
        await utils.Discord.send_help(ctx)

    @commands.check(check.acl)
    @debug_.command(name="emoji")
    async def debug_emoji(
        self, ctx, emoji: Optional[Union[discord.PartialEmoji, str]] = None
    ):
        """Debug emoji"""
        embed = utils.Discord.create_embed(
            author=ctx.author,
            title=_(ctx, "Debug - Emoji"),
            description=_(ctx, "{emoji} debug").format(emoji=str(emoji)),
        )

        embed.add_field(
            name="Class",
            value=str(type(emoji)),
        )

        ctx.send(embed)


def setup(bot) -> None:
    bot.add_cog(Debug(bot))
