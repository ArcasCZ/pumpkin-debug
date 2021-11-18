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
            title="Debug - Emoji",
            description="{emoji} debug".format(emoji=str(emoji)),
        )

        embed.add_field(
            name="Is discord.PartialEmoji",
            value=(type(emoji) is discord.PartialEmoji),
        )

        embed.add_field(
            name="Class",
            value=str(type(emoji)),
        )

        if type(emoji) == discord.PartialEmoji:
            embed.add_field(
                name="ID",
                value=emoji.id,
            )

        await ctx.send(embed=embed)

    @commands.check(check.acl)
    @debug_.command(name="str")
    async def debug_str(self, ctx, *texts):
        text = "\n".join(texts)
        await ctx.send("```" + text + "```")


def setup(bot) -> None:
    bot.add_cog(Debug(bot))
