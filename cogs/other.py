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
        await interaction.response.defer(ephemeral=False)

        # date_format = "%a, %b %d, %Y"

        embed = disnake.Embed(
            title=f"Информация о {member}",
            color=0x2f3136
        )

        embed.add_field(
            name="accent_color|accent_colour",
            value=member.accent_color,
            inline=True
        )
        embed.add_field(
            name="activities",
            value=member.activities,
            inline=True
        )
        embed.add_field(
            name="activity",
            value=member.activity,
            inline=True
        )
        embed.add_field(
            name="avatar",
            value=member.avatar,
            inline=True
        )
        embed.add_field(
            name="banner",
            value=member.banner,
            inline=True
        )
        embed.add_field(
            name="bot",
            value=member.bot,
            inline=True
        )
        embed.add_field(
            name="color|colour",
            value=member.color,
            inline=True
        )
        embed.add_field(
            name="created_at",
            value=member.created_at,
            inline=True
        )
        embed.add_field(
            name="current_timeout",
            value=member.current_timeout,
            inline=True
        )
        embed.add_field(
            name="default_avatar",
            value=member.default_avatar,
            inline=True
        )
        embed.add_field(
            name="desktop_status",
            value=member.desktop_status,
            inline=True
        )
        embed.add_field(
            name="discriminator",
            value=member.discriminator,
            inline=True
        )
        embed.add_field(
            name="display_avatar",
            value=member.display_avatar,
            inline=True
        )
        embed.add_field(
            name="display_name",
            value=member.display_name,
            inline=True
        )
        embed.add_field(
            name="dm_channel",
            value=member.dm_channel,
            inline=True
        )
        embed.add_field(
            name="flags",
            value=member.flags,
            inline=True
        )
        embed.add_field(
            name="global_name",
            value=member.global_name,
            inline=True
        )
        embed.add_field(
            name="guild",
            value=member.guild,
            inline=True
        )
        embed.add_field(
            name="guild_avatar",
            value=member.guild_avatar,
            inline=True
        )
        embed.add_field(
            name="guild_permissions",
            value=member.guild_permissions,
            inline=True
        )
        embed.add_field(
            name="id",
            value=member.id,
            inline=True
        )
        embed.add_field(
            name="joined_at",
            value=member.joined_at,
            inline=True
        )
        embed.add_field(
            name="mention",
            value=member.mention,
            inline=True
        )
        embed.add_field(
            name="mobile_status",
            value=member.mobile_status,
            inline=True
        )
        embed.add_field(
            name="mutual_guilds",
            value=member.mutual_guilds,
            inline=True
        )
        embed.add_field(
            name="name",
            value=member.name,
            inline=True
        )
        embed.add_field(
            name="nick",
            value=member.nick,
            inline=True
        )
        embed.add_field(
            name="pending",
            value=member.pending,
            inline=True
        )
        embed.add_field(
            name="premium_since",
            value=member.premium_since,
            inline=True
        )
        embed.add_field(
            name="public_flags",
            value=member.public_flags,
            inline=True
        )
        embed.add_field(
            name="raw_status",
            value=member.raw_status,
            inline=True
        )
        embed.add_field(
            name="role_icon",
            value=member.role_icon,
            inline=True
        )
        embed.add_field(
            name="roles",
            value=member.roles,
            inline=True
        )
        embed.add_field(
            name="status",
            value=member.status,
            inline=True
        )
        embed.add_field(
            name="system",
            value=member.system,
            inline=True
        )
        embed.add_field(
            name="tag",
            value=member.tag,
            inline=True
        )
        embed.add_field(
            name="top_role",
            value=member.top_role,
            inline=True
        )
        embed.add_field(
            name="voice",
            value=member.voice,
            inline=True
        )
        embed.add_field(
            name="web_status",
            value=member.web_status,
            inline=True
        )

        embed.set_thumbnail(url=member.avatar)
        await interaction.send(embed=embed, ephemeral=True)

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
                required=False
            )
        ]
    )
    async def send(self, interaction, message, channel: disnake.TextChannel = disnake.Interaction.channel):

        await interaction.response.defer(ephemeral=True)

        embed = disnake.Embed(title=f"Сообщение отправлено в канал {channel}",
                              color=0x2F3136)

        await channel.send(message)
        await interaction.response.send_message(embed=embed)

    @commands.slash_command(
        name="ping",
        description="Пинг"
    )
    async def ping(self, interaction):

        await interaction.response.defer(ephemeral=True)

        embed = disnake.Embed(title=f'Мой пинг: {self.bot.latency * 1000:.2f}мс!',
                              color=0x2F3136)

        await interaction.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(Other(bot))
