import disnake
from disnake.ext import commands


class Other(commands.Cog, name="Other"):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="servers_leave",
        description="Выйти со всех серверов, где есть бот",
        default_member_permissions=disnake.Permissions(administrator=True)
    )
    async def servers_leave(self, interaction):

        await interaction.response.defer(ephemeral=True)

        for guild in self.bot.guilds:
            if guild != interaction.guild:
                await guild.leave()

    @commands.slash_command(
        name="userinfo",
        description="Посмотреть информацию об участнике",
        options=[
            disnake.Option(
                name="member",
                description="Пользователь, чью информацию необходимо получить",
                type=disnake.OptionType.user,
                required=False
            )
        ]
    )
    async def userinfo(self, interaction, member: disnake.Member = disnake.Interaction.user):

        await interaction.response.defer(ephemeral=True)

        # date_format = "%a, %b %d, %Y"

        embed = disnake.Embed(
            title=f"Информация о {member}",
            color=0x2f3136
        )

        try:
            embed.add_field(
                name="Имя",
                value=member.name,
                inline=True
            )
        except:
            pass

        try:
            embed.add_field(
                name="Отображаемое имя",
                value=member.display_name if member.display_name != member.name else "Отсутствует",
                inline=True
            )
        except:
            pass

        try:
            embed.add_field(
                name="Упоминание",
                value=member.mention,
                inline=True
            )
        except:
            pass

        try:
            embed.add_field(
                name="Статус",
                value=member.status,
                inline=True
            )
        except:
            pass

        try:
            embed.add_field(
                name="Статус",
                value=member.activity if member.activity else "Отсутствует",
                inline=True
            )
        except:
            pass

        try:
            embed.add_field(
                name="Аватарка",
                value=member.avatar if member.avatar else "Отсутствует",
                inline=True
            )
        except:
            pass

        try:
            embed.add_field(
                name="Отображаемая аватарка",
                value=member.display_avatar if member.display_avatar else "Отсутствует",
                inline=True
            )
        except:
            pass

        try:
            embed.add_field(
                name="Стандартная аватарка",
                value=member.default_avatar,
                inline=True
            )
        except:
            pass

        try:
            embed.add_field(
                name="Баннер",
                value=member.banner if member.banner else "Отсутствует",
                inline=True
            )
        except:
            pass

        try:
            embed.add_field(
                name="Бот",
                value="Да" if member.bot else "Нет",
                inline=True
            )
        except:
            pass

        try:
            embed.add_field(
                name="Цвет",
                value=member.color if member.color else "Отсутствует",
                inline=True
            )
        except:
            pass

        try:
            embed.add_field(
                name="Дата присоединения",
                value=member.joined_at,
                inline=True
            )
        except:
            pass

        try:
            embed.add_field(
                name="Дата регистрации",
                value=member.created_at,
                inline=True
            )
        except:
            pass

        try:
            embed.add_field(
                name="Таймаут",
                value=member.current_timeout if member.current_timeout else "Отсутствует",
                inline=True
            )
        except:
            pass

        try:
            embed.add_field(
                name="Иконка роли",
                value=member.role_icon if member.role_icon else "Отсутствует",
                inline=True
            )
        except:
            pass

        try:
            embed.add_field(
                name="Роли",
                value="\n".join([role.mention for role in member.roles[:0:-1]]),
                inline=True
            )
        except:
            pass

        try:
            embed.add_field(
                name="ID",
                value=member.id,
                inline=True
            )
        except:
            pass

        try:
            embed.add_field(
                name="Дата приобретения нитро",
                value=member.premium_since if member.premium_since else "Отсутствует",
                inline=True
            )
        except:
            pass

        try:
            embed.add_field(
                name="Войс",
                value=member.voice.channel if member.voice else "Не сидит",
                inline=True
            )
        except:
            pass

        embed.set_thumbnail(url=member.avatar)
        await interaction.followup.send(embed=embed)

    @commands.slash_command(
        name="send",
        description="Отправить сообщение",
        default_member_permissions=disnake.Permissions(administrator=True),
        options=[
            disnake.Option(
                name="message",
                description="Сообщение",
                type=disnake.OptionType.string,
                required=True
            ),
            disnake.Option(
                name="channel",
                description="Канал, куда отправить",
                type=disnake.OptionType.channel,
                required=True
            )
        ]
    )
    async def send(self, interaction, message, channel):

        await interaction.response.defer(ephemeral=True)

        embed = disnake.Embed(title=f"Сообщение отправлено в канал {channel}",
                              color=0x2F3136)

        await channel.send(message)

        await interaction.followup.send(embed=embed)

    @commands.slash_command(
        name="ping",
        description="Пинг"
    )
    async def ping(self, interaction):

        await interaction.response.defer(ephemeral=True)

        embed = disnake.Embed(title=f'Мой пинг: {self.bot.latency * 1000:.2f}мс!',
                              color=0x2F3136)

        await interaction.followup.send(embed=embed)


def setup(bot):
    bot.add_cog(Other(bot))
