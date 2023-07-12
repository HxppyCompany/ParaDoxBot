import datetime
import random

import disnake
from disnake import Embed
from disnake.ext import commands

from cogs.variables import Roles
from cogs.variables import DataBase
from cogs.variables import System


async def ifstaff(interaction, member):
    staff_role = interaction.guild.get_role(Roles.staff)
    if staff_role in member.roles:
        embed = Embed(title=f"Нельзя наказать персонал",
                      color=0x2F3136)
        await interaction.send(embed=embed, ephemeral=True)
        return True
    else:
        return False


async def adds(embed):
    add = random.randint(1, 2)
    if add == 1:
        embed.set_author(name="Приобрести рекламу в боте можно у HappyFan",
                         url="",
                         icon_url="")
    if add == 2:
        embed.set_author(name="Здесь могла быть ваша реклама",
                         url="",
                         icon_url="")


class Moderation(commands.Cog, name="Moderation"):
    def __init__(self, bot):
        self.bot = bot

    '''Mute'''

    @commands.slash_command(
        name="mute",
        description="Выдать мут указанному пользователю на заданный срок по указанной причине",
        default_member_permissions=disnake.Permissions(moderate_members=True),
        options=[
            disnake.Option(
                name="member",
                description="Наказуемый пользователь",
                type=disnake.OptionType.user,
                required=True
            ),
            disnake.Option(
                name="time",
                description="Длительность наказания (m/h/d / м/ч/д)",
                type=disnake.OptionType.string,
                required=True
            ),
            disnake.Option(
                name="reason",
                description="Причина выдачи наказания",
                type=disnake.OptionType.string,
                required=True
            )
        ]
    )
    async def mute(self, interaction, member, time=None, reason=None):

        if await ifstaff(interaction, member):
            return

        # VARIABLES
        interval = None if time.isdigit() else time[-1]
        word = None
        number = None
        duration = None
        username = member.name
        moderator = interaction.author
        msg: disnake.Message = interaction.target

        # INTERVAL
        if interval is None:
            number = int(time)
            word = "час" if number == 1 else ("часа" if word in range(2, 5) else "часов")
            duration = datetime.timedelta(hours=number)
        else:
            number = int(time[:-1])
            if interval in ["m", "м"]:
                word = "минуту" if number == 1 else ("минуты" if word in range(2, 5) else "минут")
                duration = datetime.timedelta(minutes=number)
            elif interval in ["h", "ч"]:
                word = "час" if number == 1 else ("часа" if word in range(2, 5) else "часов")
                duration = datetime.timedelta(hours=number)
            elif interval in ["d", "д"]:
                word = "день" if number == 1 else ("дня" if word in range(2, 5) else "дней")
                duration = datetime.timedelta(days=number)
            else:
                embed = Embed(title="Вы указали неверный промежуток времени",
                              color=0x2F3136)
                await interaction.send(embed=embed)
                return

        # EMBED
        embed = Embed(title=f"{username} получил мут",
                      description="",
                      color=0x2F3136)
        embed.add_field(name=f"ДЛИТЕЛЬНОСТЬ",
                        value=f"```{number} {word}```",
                        inline=True)
        embed.add_field(name=f"ПРИЧИНА",
                        value=f"```{reason}```",
                        inline=True)
        embed.set_footer(text=f"{moderator}",
                         icon_url=interaction.author.avatar)

        await adds(embed=embed)

        await member.timeout(duration=duration, reason=f"{moderator}: {reason}")
        await interaction.send(embed=embed, delete_after=60)

    '''Unmute'''

    @commands.slash_command(
        name="unmute",
        description="Снять мут указанному пользователю по указанной причине",
        default_member_permissions=disnake.Permissions(moderate_members=True),
        options=[
            disnake.Option(
                name="member",
                description="Наказанный пользователь",
                type=disnake.OptionType.user,
                required=True
            ),
            disnake.Option(
                name="reason",
                description="Причина снятия наказания",
                type=disnake.OptionType.string,
                required=False
            )
        ]
    )
    async def unmute(self, interaction, member, reason=None):

        if await ifstaff(interaction, member):
            return

        # VARIABLES
        username = member.name
        moderator = interaction.author

        # EMBED
        embed = Embed(title=f"{username} сняли мут",
                      description="",
                      color=0x2F3136)
        embed.set_footer(text=f"{moderator}",
                         icon_url=interaction.author.avatar)

        # REASON
        if reason is not None:
            embed.add_field(name=f"ПРИЧИНА",
                            value=f"```{reason}```",
                            inline=True)
        else:
            reason = "без указания причины"

        await adds(embed)

        await member.timeout(duration=None, reason=f'{moderator}: {reason}')
        await interaction.send(embed=embed, delete_after=60)

    '''Ban'''

    @commands.slash_command(
        name="ban",
        description="Выдать блокировку указанному пользователю по указанной причине",
        default_member_permissions=disnake.Permissions(ban_members=True),
        options=[
            disnake.Option(
                name="member",
                description="Наказуемый пользователь",
                type=disnake.OptionType.user,
                required=True
            ),
            disnake.Option(
                name="reason",
                description="Причина выдачи наказания",
                type=disnake.OptionType.string,
                required=True
            )
        ]
    )
    async def ban(self, interaction, member, reason):

        if await ifstaff(interaction, member):
            return

        # VARIABLES
        username = member.name
        moderator = interaction.author

        # EMBED
        embed = Embed(title=f"{username} получил бан",
                      description="",
                      color=0x2F3136)
        embed.add_field(name=f"ПРИЧИНА",
                        value=f"```{reason}```",
                        inline=True)
        embed.set_footer(text=f"{moderator}",
                         icon_url=interaction.author.avatar)

        await adds(embed)

        for i in member.roles:
            await member.remove_roles(i)
        await member.add_roles(interaction.guild.get_role(Roles.localban))

        if DataBase.localban.count_documents({"_id": member.id}) == 0:
            post = {
                "_id": member.id,
                "name": member.name,
                "localban": True,
                "issued_by": interaction.author.id,
                "timestamp": interaction.created_at.strftime(System.date_format)
            }
            DataBase.localban.insert_one(post)

        await interaction.send(embed=embed, delete_after=60.0)

    '''Unban'''

    @commands.slash_command(
        name="unban",
        description="Снять блокировку указанному пользователю по указанной причине",
        default_member_permissions=disnake.Permissions(ban_members=True),
        options=[
            disnake.Option(
                name="member",
                description="Наказанный пользователь",
                type=disnake.OptionType.user,
                required=True
            ),
            disnake.Option(
                name="reason",
                description="Причина снятия наказания",
                type=disnake.OptionType.string,
                required=False
            )
        ]
    )
    async def unban(self, interaction, member, reason=None):

        if await ifstaff(interaction, member):
            return

        # VARIABLES
        username = member.name
        moderator = interaction.author

        # EMBED
        embed = Embed(title=f"{username} сняли бан",
                      description="",
                      color=0x2F3136)
        embed.set_footer(text=f"{moderator}",
                         icon_url=interaction.author.avatar)

        # REASON
        if reason is not None:
            embed.add_field(name=f"ПРИЧИНА",
                            value=f"```{reason}```",
                            inline=True)
        else:
            reason = "без указания причины"

        await adds(embed)

        await member.remove_roles(interaction.guild.get_role(Roles.localban))
        await member.add_roles(interaction.guild.get_role(Roles.unverify))

        if DataBase.localban.count_documents({"_id": member.id}) != 0:
            DataBase.localban.remove_one({"_id": member.id})

        await interaction.send(embed=embed, delete_after=60)

    '''Kick'''

    @commands.slash_command(
        name="kick",
        description="Выгнать указанного пользователя по указанной причине",
        default_member_permissions=disnake.Permissions(kick_members=True),
        options=[
            disnake.Option(
                name="member",
                description="Наказуемый пользователь",
                type=disnake.OptionType.user,
                required=True
            ),
            disnake.Option(
                name="reason",
                description="Причина выдачи наказания",
                type=disnake.OptionType.string,
                required=True
            )
        ]
    )
    async def kick(self, interaction, member, reason):

        if await ifstaff(interaction, member):
            return

        # VARIABLES
        username = member.name
        moderator = interaction.author

        # EMBED
        embed = Embed(title=f"{username} выгнан",
                      description="",
                      color=0x2F3136)
        embed.add_field(name=f"ПРИЧИНА",
                        value=f"```{reason}```",
                        inline=True)
        embed.set_footer(text=f"{moderator}",
                         icon_url=interaction.author.avatar)

        # PROOF
        if interaction.target.reference and isinstance(interaction.target.reference.resolved, disnake.Message):
            embed.add_field(name=f"ДОКАЗАТЕЛЬСТВО",
                            value=f"```{interaction.target.reference.resolved.content}```",
                            inline=True)

        await adds(embed)

        await member.kick(reason=f'{moderator}: {reason}')
        await interaction.send(embed, delete_after=60)


def setup(bot):
    bot.add_cog(Moderation(bot))
