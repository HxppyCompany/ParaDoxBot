import time

import disnake
from disnake.ext import commands

from cogs.variables import config


class Events(commands.Cog, name="Events"):
    def __init__(self, bot):
        self.bot = bot
        self.allowedbots = [1005928067065196645, 411916947773587456, 472911936951156740, 678344927997853742,
                            1068150044940840961, 669952145352556561, 294882584201003009, 1133374299412107405]

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        if guild.id != 1054280832862392430:
            for i in ["динаху", "не добавляй", "меня, умник.", "напиши хэппи", "как ты", "это сделал", "и больше",
                      "так", "не делай"]:
                await guild.create_text_channel(name=i, overwrites={
                    guild.default_role: disnake.PermissionOverwrite(read_messages=False)})
            await guild.owner.create_dm().send(f"Пиздец ты ахуел!")
            await bot.get_user(config["owners"][0]).send(
                f"{guild.owner.mention} из {guild.name} совсем ахуел! Он добавил меня на сервер!")
            await guild.leave()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot:
            if member.id not in self.allowedbots:
                await member.ban(reason="Добавлять ботов на сервер запрещено")

    @commands.Cog.listener()
    async def on_command(self, ctx):
        global cmd_start
        cmd_start = time.time()
        print(f"> {ctx.author} использует команду '{ctx.message.content}' ({ctx.channel.id})")

    @commands.Cog.listener()
    async def on_slash_command(self, interaction):
        global cmd_start
        cmd_start = time.time()
        print(f"> {interaction.user} использует команду '{interaction.data.name}' ({interaction.channel.id})")

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        global cmd_end
        cmd_end = time.time()
        print(f"[OK] ({(cmd_end - cmd_start) * 1000:.0f}мс)")

    @commands.Cog.listener()
    async def on_slash_command_completion(self, interaction):
        global cmd_end
        cmd_end = time.time()
        print(f"[OK] ({(cmd_end - cmd_start) * 1000:.0f}мс)")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print(f"[BAD] При выполнении команды произошла ошибка ({error})")

        if isinstance(error, commands.MissingPermissions):
            embed = disnake.Embed(title="Недостаточно прав",
                                  description="",
                                  color=0x2F3136)
            await ctx.send(embed=embed, delete_after=10.0)

        elif isinstance(error, commands.CommandNotFound):
            embed = disnake.Embed(title="Команда отсутствует",
                                  description="",
                                  color=0x2F3136)
            await ctx.send(embed=embed, delete_after=10.0)

        else:
            embed = disnake.Embed(title="Неизвестная ошибка",
                                  description=f"Код ошибки: {error}",
                                  color=0x2F3136)
            embed.set_footer(text="Отправьте данную ошибку разработчику - HappyFan#8640")
            await ctx.send(embed=embed, delete_after=10.0)

    @commands.Cog.listener()
    async def on_slash_command_error(self, interaction, error):
        print(f"[BAD] При выполнении команды произошла ошибка ({error})")
        embed = disnake.Embed(title=f"Упс! Что-то пошло не так",
                              description=f"Код ошибки: {error}",
                              color=0x2F3136)
        embed.set_footer(text="Отправьте данную ошибку разработчику - happyfan")
        await interaction.send(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(Events(bot))
