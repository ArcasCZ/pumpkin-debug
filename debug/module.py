import datetime
import random
import re
import tempfile
import urllib
from typing import Optional, Union, Dict, List
from PIL import Image, ImageFile

import nextcord
from nextcord.ext import commands, tasks

from pie import utils, check, storage
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

    @check.acl2(check.ACLevel.BOT_OWNER)
    @debug_.command(name="str")
    async def debug_str(
        self, ctx: commands.Context, *members: Union[nextcord.Member, int]
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
        HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}
    async def debug_message(self, ctx: commands.Context, message: nextcord.Message):
        pass

    @check.acl2(check.ACLevel.BOT_OWNER)
    @debug_.command(name="channels")
    async def debug_channels(self, ctx):
        channel_count = len(ctx.guild.channels)
        await ctx.send(f"There are {channel_count} channels.")


def setup(bot) -> None:
    bot.add_cog(Debug(bot))
