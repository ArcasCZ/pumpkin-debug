import tempfile
from typing import Optional, Union

import discord
from discord.ext import commands

from pie import utils, check
from pie.database import session

from modules.school.review.database import SubjectReview, TeacherReview


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

    @check.acl2(check.ACLevel.BOT_OWNER)
    @debug_.command(name="review")
    async def debug_review(self, ctx):
        reviews = []
        subject_reviews = (
            session.query(SubjectReview).filter_by(guild_id=ctx.guild.id).all()
        )
        for review in subject_reviews:
            reviews.append(
                "subject;{abbreviation};{name};{text}".format(
                    abbreviation=review.subject.abbreviation,
                    name=review.subject.name,
                    text=review.text_review.replace("\n", "\t"),
                )
            )

        teacher_reviews = (
            session.query(TeacherReview).filter_by(guild_id=ctx.guild.id).all()
        )
        for review in teacher_reviews:
            reviews.append(
                "subject;{id};{name};{text}".format(
                    id=review.teacher.school_id,
                    name=review.teacher.name,
                    text=review.text_review.replace("\n", "\t").replace(";", "."),
                )
            )

        file = tempfile.TemporaryFile(mode="w+")

        file.write("Type;ID;Name;Text\n" + "\n".join(reviews))

        filename = "review_dump.csv"

        file.seek(0)
        await ctx.reply(
            "Message exported to CSV.",
            file=discord.File(fp=file, filename=filename),
        )
        file.close()


async def setup(bot) -> None:
    await bot.add_cog(Debug(bot))
