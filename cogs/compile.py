import subprocess

import disnake
from disnake.ext import commands


class Compile(commands.Cog, name='Compile'):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="compile",
        description="Выполнить команду в консоли бота",
        options=[
            disnake.Option(
                name="command",
                description="Консольная команда",
                type=disnake.OptionType.string,
                required=True
            )
        ]
    )
    async def compile(self, interaction, command):
        if interaction.user.id in self.bot.config["owners"]:
            await interaction.response.defer(ephemeral=True)
            print(f"[CMD] {command}")
            subprocess.run(command, shell=True)
            embed = disnake.Embed(title=f"Команда `{command}` выполнена успешно!", description="", color=0x2F3136)
        else:
            embed = disnake.Embed(title="Недостаточно прав", description="", color=0x2F3136)
        await interaction.edit_original_response(embed=embed)
        
    @commands.slash_command(
        name="git_upload",
        description="Обновить версию бота на GitHub, загрузив все файлы с хостинга"
    )
    async def git_upload(self, interaction):
        if interaction.user.id in self.bot.config["owners"]:
            await interaction.response.defer(ephemeral=True)
            subprocess.run("git add . && git status && git commit -m 'commit' && git push origin main", shell=True)
            embed = disnake.Embed(title=f"Версия бота на GitHub успешно обновлена!", description="", color=0x2F3136)
        else:
            embed = disnake.Embed(title="Недостаточно прав", description="", color=0x2F3136)
        await interaction.edit_original_response(embed=embed)


def setup(bot):
    bot.add_cog(Compile(bot))
