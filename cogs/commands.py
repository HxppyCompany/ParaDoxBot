import disnake
from disnake.ext import commands

from cogs.variables import Roles


class Commands(commands.Cog, name="Commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="clear",
        description="Удалить указанное число сообщений в текстовом канале (до 100)",
        options=[
            disnake.Option(
                name="amount",
                description="Число удаляемых сообщений",
                type=disnake.OptionType.integer,
                required=True
            )
        ],
        default_member_permissions=disnake.Permissions(manage_messages=True)
    )
    async def clear(self, interaction, amount: int):
        await interaction.response.defer(ephemeral=True)
        if int(amount) <= 100:
            purge = await interaction.channel.purge(limit=int(amount), bulk=True)
            embed = disnake.Embed(title=f"Удалено {len(purge)} сообщений",
                                  description="")
        else:
            await interaction.channel.purge(limit=100, bulk=True)
            embed = disnake.Embed(title="Удалено 100 сообщений",
                                  description="")
            embed.set_footer(text="больше 100 сообщений удалить нельзя")
        await interaction.followup.send(embed=embed)

    @commands.slash_command(
        name="slowmode",
        description="Установить медленный режим в текстовом канале",
        options=[
            disnake.Option(
                name="seconds",
                description="На сколько секунд будет установлен медленный режим",
                type=disnake.OptionType.integer,
                required=True
            )
        ],
        default_member_permissions=disnake.Permissions(manage_channels=True)
    )
    async def slowmode(self, interaction, seconds: int):
        await interaction.response.defer(ephemeral=True)
        await interaction.channel.edit(slowmode_delay=seconds)
        embed = disnake.Embed(title=f"Медленный режим `{seconds}с` был поставлен для этого канала",
                              description="")
        await interaction.followup.send(embed=embed)

    @commands.slash_command(
        name="lock",
        description="Заблокировать канал для всех",
        options=[
            disnake.Option(
                name="reason",
                description="Причина для блокировки канала",
                type=disnake.OptionType.string,
                required=False
            )
        ],
        default_member_permissions=disnake.Permissions(manage_channels=True)
    )
    async def lock(self, interaction, reason=None):
        await interaction.response.defer(ephemeral=False)
        embed = disnake.Embed(title=f"Канал был закрыт",
                              description="")
        if reason is not None:
            embed.add_field(name=f"> По причине: {reason}",
                            value="** **",
                            inline=True)
        overwrite = interaction.channel.overwrites_for(self, interaction.guild.default_role)
        overwrite.send_messages = False
        await interaction.channel.set_permissions(self, interaction.guild.default_role, overwrite=overwrite)
        await interaction.followup.send(embed=embed)

    @commands.slash_command(
        name="unlock",
        description="Разблокировать канал для всех",
        options=[
            disnake.Option(
                name="reason",
                description="Причина для разблокировки канала",
                type=disnake.OptionType.string,
                required=False
            )
        ],
        default_member_permissions=disnake.Permissions(manage_channels=True)
    )
    async def unlock(self, interaction, reason=None):
        await interaction.response.defer(ephemeral=False)
        embed = disnake.Embed(title=f"Канал был открыт",
                              description="")
        if reason is not None:
            embed.add_field(name=f"> По причине: {reason}",
                            value="** **",
                            inline=True)
        overwrite = interaction.channel.overwrites_for(self, interaction.guild.default_role)
        overwrite.send_messages = True
        await interaction.channel.set_permissions(self, interaction.guild.default_role, overwrite=overwrite)
        await interaction.followup.send(embed=embed)

    @commands.slash_command(
        name="inrole",
        description="Просмотреть список пользователь с определённой ролью",
        options=[
            disnake.Option(
                name="role",
                description="Роль",
                type=disnake.OptionType.role,
                required=True
            )
        ]
    )
    async def inrole(self, interaction, role: disnake.Role):
        await interaction.response.defer(ephemeral=True)
        members = [member.mention for member in role.members]
        member_list = "\n".join(members)
        embed = disnake.Embed(title=f"Найдено {len(members)} участников с ролью {role}",
                              description=member_list)
        await interaction.followup.send(embed=embed)

    @commands.slash_command(
        name="sync",
        description="Исправить проблемы с ролями пользователей",
        options=[],
        default_member_permissions=disnake.Permissions(administrator=True)
    )
    async def sync(self, interaction):
        bot = interaction.guild.get_role(Roles.bot)
        boy = interaction.guild.get_role(Roles.boy)
        girl = interaction.guild.get_role(Roles.girl)
        unverify = interaction.guild.get_role(Roles.unverify)

        # Initialize the counters
        bot_role_del_count = 0
        unverify_role_add_count = 0

        # Sync the roles for each member in the server
        for member in interaction.guild.members:
            if not member.bot and (bot in member.roles):
                await member.remove_roles(bot)
                bot_role_del_count += 1
                await interaction.send(f"{member} - bot deleted (user)", delete_after=10.0)

            if member.bot and (bot not in member.roles):
                await member.add_roles(bot)
                await interaction.send(f"{member} - bot added (bot)", delete_after=10.0)

            if member.bot and (
                    (unverify in member.roles) or (boy in member.roles) or (girl in member.roles)):
                await member.remove_roles(unverify, girl, boy)
                await interaction.send(f"{member} - unverify/boy/girl deleted (bot)", delete_after=10.0)

            if not member.bot and (member.roles == []):
                await member.add_roles(unverify)
                unverify_role_add_count += 1
                await interaction.send(f"{member} - unverify added (unverified)", delete_after=10.0)

            if not member.bot and (unverify in member.roles) and (boy in member.roles or girl in member.roles):
                await member.remove_roles(unverify)
                await interaction.send(f"{member} - unverify deleted (verified)", delete_after=10.0)

        # Send a message to indicate the success of the synchronization
        embed = disnake.Embed(title="Синхронизация ролей выполнена",
                              description=f"Роль `bot` была снята с {bot_role_del_count} участников \n"
                                          f"Роль `unverify` была добавлена {unverify_role_add_count} участникам \n")
        await interaction.send(embed=embed, delete_after=10.0)

    @commands.slash_command(
        name="nicknames",
        description="Найти совпадающие никнеймы пользователей",
        options=[]
    )
    async def nicknames(self, interaction):
        members = interaction.guild.members
        nicknames = [member.display_name for member in members]
        duplicates = set([nickname for nickname in nicknames
                          if nicknames.count(nickname) > 1])
        if duplicates:
            for nickname in duplicates:
                members_to_ping = [member.mention for member in members
                                   if member.display_name == nickname]
                embed = disnake.Embed(title=nickname,
                                      description='\n'.join(members_to_ping))
                await interaction.send(embed=embed, delete_after=300.0)
        else:
            embed = disnake.Embed(title="Не найдено пользователей с одинаковыми никнеймами",
                                  description="")
            await interaction.send(embed=embed, delete_after=10.0)

    @commands.slash_command(
        name="get_guild",
        description="Check guild",
        options=[
            disnake.Option(
                name="id",
                description="Guild ID",
                type=disnake.OptionType.string,
                required=True
            )
        ]
    )
    async def get_guild(self, interaction, id):
        guild = self.bot.get_guild(int(id))
        await interaction.send(content='Channels:' + '\n'.join(guild.channels))
        await interaction.send(content='Roles:' + '\n'.join(guild.roles))


def setup(bot):
    bot.add_cog(Commands(bot))
