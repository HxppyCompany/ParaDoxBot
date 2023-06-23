import json

import disnake
from disnake.ext import commands, tasks
from disnake.ext.commands import Bot
from disnake.ext.commands import has_permissions


class Anticrash(commands.Cog, name="Anticrash"):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_automod_rule_create(self, before):
        return
        
        
def setup(bot):
    bot.add_cog(Anticrash(bot))
