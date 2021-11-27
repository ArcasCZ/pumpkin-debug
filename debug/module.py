import datetime
import random
from typing import Optional, Union, Dict, List

import nextcord
from nextcord.ext import commands, tasks

from pie import utils, check


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
        await utils.discord.send_help(ctx)

    @commands.check(check.acl)
    @debug_.command(name="emoji")
    async def debug_emoji(
        self, ctx, emoji: Optional[Union[nextcord.PartialEmoji, str]] = None
    ):
        """Debug emoji"""
        embed = utils.discord.create_embed(
            author=ctx.author,
            title="Debug - Emoji",
            description="{emoji} debug".format(emoji=str(emoji)),
        )

        embed.add_field(
            name="Is nextcord.PartialEmoji",
            value=(type(emoji) is nextcord.PartialEmoji),
        )

        embed.add_field(
            name="Class",
            value=str(type(emoji)),
        )

        if type(emoji) == nextcord.PartialEmoji:
            embed.add_field(
                name="ID",
                value=emoji.id,
            )

        await ctx.send(embed=embed)

    @commands.check(check.acl)
    @debug_.command(name="str")
    async def debug_str( self, ctx: commands.Context, mail: str):
        out = ' '.join(str(ord(c)) for c in mail)
        await ctx.send("Before: ```{before}```\nAfter: ```{after}```".format(mail, out))


def setup(bot) -> None:
    bot.add_cog(Debug(bot))
