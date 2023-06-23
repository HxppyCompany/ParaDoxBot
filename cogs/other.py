import json
import os
import platform
import random
import sys
import io
import asyncio
import shutil
import time

import disnake
from disnake.ext import commands, tasks
from disnake.ext.commands import Bot
import datetime
from disnake.ext.commands import has_permissions


class Other(commands.Cog, name="Other"):
    def __init__(self, bot):
        self.bot = bot
        self.BACKUP_DIR = "backup/"
        self.allowedbots = [1005928067065196645, 411916947773587456, 472911936951156740, 678344927997853742,
                            1068150044940840961, 669952145352556561, 294882584201003009]

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def serversleave(self, ctx):
        for guild in self.bot.guilds:
            await guild.leave()

    @commands.command()
    async def userinfo(self, ctx: commands.Context, member: disnake.Member = None):
        await ctx.message.delete()
        if ctx.message.channel == ctx.guild.get_channel(1054280833533485089):
            date_format = "%a, %b %d, %Y"
            if not member:
                member = ctx.message.author
            embed = disnake.Embed(
                title=f"Информация о {member}",
                color=0x2f3136
            )
            embed.add_field(
                name=f" > Аккаунт был создан {member.created_at.strftime(date_format)} \n"
                     f" > Зашёл на сервер {member.joined_at.strftime(date_format)} \n"
                     f" > Его айди: {member.id}",
                value="** **", inline=True)
            embed.set_thumbnail(url=member.avatar)
            await ctx.send(embed=embed)
        elif ctx.message.channel != ctx.guild.get_channel(1054280833533485089):
            embed = disnake.Embed(title=f"Канал для команд: {ctx.guild.get_channel(1054280833533485089).name}")
            await ctx.send(embed=embed, delete_after=300.0)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def sendmessage(self, ctx: commands.Context, *, arg1):
        await ctx.message.delete()
        await ctx.send(arg1)
        
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def sendembed(self, ctx: commands.Context, *, arg1):
        await ctx.message.delete()
        embed = disnake.Embed(title="",
                             description=arg1)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def sendmessageid(self, ctx: commands.Context, channelid: int, *, arg1):
        await ctx.message.delete()
        channel = self.bot.get_channel(channelid)
        await channel.send(arg1)

    @commands.command()
    async def ping(self, ctx):
        await ctx.message.delete()
        embed = disnake.Embed(title=f'Мой пинг: {self.bot.latency * 1000:.2f}мс!',
                              color=0x2F3136)
        await ctx.send(embed=embed, delete_after=300.0)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def backup(self, ctx):
        """
        Performs a backup of the server data.
        """
        # Create backup directory if it doesn't exist
        if not os.path.exists(self.BACKUP_DIR):
            os.mkdir(self.BACKUP_DIR)

        # Copy server data to backup directory
        shutil.copytree(".", self.BACKUP_DIR + time.strftime("%Y-%m-%d-%H-%M-%S"))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def restore(self, ctx):
        """
        Restores the server data from the most recent backup.
        """
        # Find the most recent backup directory
        self.BACKUP_DIRs = os.listdir(self.BACKUP_DIR)
        self.BACKUP_DIRs.sort(reverse=True)
        latest_backup = os.path.join(self.BACKUP_DIR, self.BACKUP_DIRs[0])

        # Restore server data from backup
        shutil.rmtree(".")
        shutil.copytree(latest_backup, ".")


def setup(bot):
    bot.add_cog(Other(bot))
