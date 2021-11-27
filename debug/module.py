import datetime
import random
import re
import tempfile
import urllib
from typing import Optional, Union, Dict, List
from PIL import Image, ImageFile

import nextcord
from nextcord.ext import commands, tasks

from pie import utils, check
from pie.database import session

MAX_ATTACHMENT_SIZE = 8000
ALLOWED_FORMATS = ("jpg", "jpeg", "png", "webp", "gif")


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
    async def debug_str( self, ctx: commands.Context, *members: Union[nextcord.Member, int]):
        for member in members:
            if isinstance(member, int):
                member_id = member
                member = ctx.guild.get_member(member_id)
            else:
                member_id = member.id
                
            print("{}, {}".format(member, member_id))
            

    @commands.check(check.acl)
    @debug_.command(name="message")
    async def debug_message( self, ctx: commands.Context, message: nextcord.Message):
        
        """opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36')]
        urllib.request.install_opener(opener)"""
        HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}
        
        for url in re.findall(r'(https?://[^\s]+)', message.content):
            print(url)
            req = urllib.request.Request(url, headers=HEADERS)
            file = urllib.request.urlopen(req, timeout=20)
            size = file.headers.get("content-length")
            if size: size = int(size)
            
            if not size or size > MAX_ATTACHMENT_SIZE * 1024:
                print("Too fat")
                continue
                
            type = file.headers.get("content-type").split("/")
            
            if len(type) != 2 or type[0] != "image" or type[1] not in ALLOWED_FORMATS:
                print("Not allowed")
                continue
                
            parser = ImageFile.Parser()
            
            downloaded = 0
            
            while downloaded <= MAX_ATTACHMENT_SIZE:
                data = file.read(1024)
                downloaded += 1
                if not data:
                    break
                parser.feed(data)
            file.close()
            
            try:
                image = parser.close()
            except OSError:
                print("Error")
                continue
                
            print(image)
        print("Done")


def setup(bot) -> None:   
    bot.add_cog(Debug(bot))
