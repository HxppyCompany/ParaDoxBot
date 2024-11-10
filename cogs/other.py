import disnake
from disnake.ext import commands


class Other(commands.Cog, name="Other"):
    def __init__(self, bot):
        self.bot = bot

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
