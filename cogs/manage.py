import disnake
from disnake.ext import commands


class Manage(commands.Cog, name="Manage"):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="delete_channel",
        description="Удалить канал",
        options=[
            disnake.Option(
                name="channel",
                description="Канал",
                type=disnake.OptionType.channel,
                required=True
            )
        ],
        default_member_permissions=disnake.Permissions(manage_channels=True)
    )
    async def delete_channel(self, interaction, channel):
        embed = disnake.Embed(title=f"Канал **{channel.name}** удалён",
                              description="",
                              color=0x2F3136)
        await interaction.send(embed=embed,
                               delete_after=300.0)
        await channel.delete()

    @commands.slash_command(
        name="create_channel",
        description="Создать канал",
        options=[
            disnake.Option(
                name="name",
                description="Название канала",
                type=disnake.OptionType.string,
                required=True
            ),
            disnake.Option(
                name="category",
                description="Категория, в которой будет создан канал",
                type=disnake.OptionType.channel,
                required=True
            )
        ],
        default_member_permissions=disnake.Permissions(manage_channels=True)
    )
    async def create_channel(self, interaction, name, category):
        if isinstance(category, disnake.CategoryChannel):
            channel = await interaction.guild.create_text_channel(name=name, category=category)
            embed = disnake.Embed(title=f"Канал **{channel.mention}** создан в категории **{category.name}**",
                                  description="",
                                  color=0x2F3136)
            await interaction.send(embed=embed,
                                   delete_after=300.0)
        else:
            embed = disnake.Embed(title=f"**{category}** не является категорией",
                                  description="",
                                  color=0x2F3136)
            await interaction.send(embed=embed,
                                   delete_after=10.0)

    @commands.slash_command(
        name="create_category",
        description="Создать категорию",
        options=[
            disnake.Option(
                name="name",
                description="Название категории",
                type=disnake.OptionType.string,
                required=True
            )
        ],
        default_member_permissions=disnake.Permissions(manage_channels=True)
    )
    async def create_category(self, interaction, name):
        category = await interaction.guild.create_category(name)
        embed = disnake.Embed(title=f"Категория **{category.name}** создана",
                              description="",
                              color=0x2F3136)
        await interaction.send(embed=embed,
                               delete_after=300.0)

    @commands.slash_command(
        name="delete_category",
        description="Удалить категорию",
        options=[
            disnake.Option(
                name="category",
                description="ID категории",
                type=disnake.OptionType.channel,
                required=True
            )
        ],
        default_member_permissions=disnake.Permissions(manage_channels=True)
    )
    async def delete_category(self, interaction, category):
        if isinstance(category, disnake.CategoryChannel):
            embed = disnake.Embed(title=f"Категория **{category.name}** удалена",
                                  description="",
                                  color=0x2F3136)
            await category.delete()
            await interaction.send(embed=embed,
                                   delete_after=300.0)
        else:
            embed = disnake.Embed(title=f"**{category}** не является категорией",
                                  description="",
                                  color=0x2F3136)
            await interaction.send(embed=embed,
                                   delete_after=10.0)


def setup(bot):
    bot.add_cog(Manage(bot))
