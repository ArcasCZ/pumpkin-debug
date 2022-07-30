import datetime
import random
import re
import tempfile
import urllib
from typing import Optional, Union, Dict, List
from PIL import Image, ImageFile

import discord
from discord.ext import commands, tasks

from pie import utils, check
from pie.database import session


class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Commands

    @commands.guild_only()
    @commands.group(name="debug")
    @check.acl2(check.ACLevel.BOT_OWNER)
    async def debug_(self, ctx):
        """Debug tools"""
        await utils.discord.send_help(ctx)

    @check.acl2(check.ACLevel.BOT_OWNER)
    @debug_.command(name="emoji")
    async def debug_emoji(
        self, ctx, emoji: Optional[Union[discord.PartialEmoji, str]] = None
    ):
        """Debug emoji"""
        embed = utils.discord.create_embed(
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

    @check.acl2(check.ACLevel.BOT_OWNER)
    @debug_.command(name="str")
    async def debug_str(
        self, ctx: commands.Context, *members: Union[discord.Member, int]
    ):
        for member in members:
            if isinstance(member, int):
                member_id = member
                member = ctx.guild.get_member(member_id)
            else:
                member_id = member.id

            print("{}, {}".format(member, member_id))

    @check.acl2(check.ACLevel.BOT_OWNER)
    @debug_.command(name="message")
    async def debug_message(self, ctx: commands.Context, message: discord.Message):
        pass

    @check.acl2(check.ACLevel.BOT_OWNER)
    @debug_.command(name="channels")
    async def debug_channels(self, ctx):
        channel_count = len(ctx.guild.channels)
        await ctx.send(f"There are {channel_count} channels.")


async def setup(bot) -> None:
    await bot.add_cog(Debug(bot))
