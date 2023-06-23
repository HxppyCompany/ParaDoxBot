import json
import os
import asyncio
import subprocess

import disnake
from disnake.ext import commands, tasks
from disnake.ext.commands import Bot
from disnake.ext.commands import has_permissions

import cogs.variables
from cogs.variables import System
from cogs.variables import DataBase
from cogs.variables import Guild
from cogs.variables import Roles
from cogs.variables import Staff
from cogs.variables import Channels
# from cogs.variables import Templates

'''BUTTONS'''


class GirlButton(disnake.ui.Button):
    def __init__(self, user):
        super().__init__(style=disnake.ButtonStyle.blurple, label="Девушка", custom_id="verifyg")
        self.user = user

    async def callback(self, interaction):
        member = interaction.guild.get_member(self.user.id)
        staff = interaction.guild.get_role(Staff.validator)
        if staff not in interaction.user.roles:
            embed = disnake.Embed(title="Недостаточно прав",
                                  description="")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        verify_chs = [interaction.guild.get_channel(i) for i in Channels.verify]
        member_in_voice = False
        for ch in verify_chs:
            if member in ch.members:
                member_in_voice = True
        if not member_in_voice:
            embed = disnake.Embed(title="Человек не в голосовом канале",
                                  description="")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        try:
            unverify = interaction.guild.get_role(Roles.unverify)
            await member.remove_roles(unverify)
        except:
            pass
        role = interaction.guild.get_role(Roles.girl)
        await member.add_roles(role)
        await interaction.message.edit(view=None)
        embed = disnake.Embed(title=f"{member} была верефицирована валидатором {interaction.user}",
                              description="")
        await interaction.response.send_message(embed=embed)
        try:
            mEmbed = disnake.Embed(title=f"Валидатор {interaction.user} верифицировал тебя",
                                   description="Пожалуйста, оцените его работу ниже по 5-ти балльной шкале\n"
                                               "Приятного времяпрепровождения на нашем сервере!")
            await member.send(embed=mEmbed, view=RateView(user=member, validator=interaction.user))
        except Exception as e:
            print(f"[ERROR] {e}")


class BoyButton(disnake.ui.Button):
    def __init__(self, user):
        super().__init__(style=disnake.ButtonStyle.blurple, label="Парень", custom_id="verifym")
        self.user = user

    async def callback(self, interaction):
        member = interaction.guild.get_member(self.user.id)
        staff = interaction.guild.get_role(Staff.validator)
        if staff not in interaction.user.roles:
            embed = disnake.Embed(title="Недостаточно прав",
                                  description="")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        verify_chs = [interaction.guild.get_channel(i) for i in Channels.verify]
        member_in_voice = False
        for ch in verify_chs:
            if member in ch.members:
                member_in_voice = True
        if not member_in_voice:
            embed = disnake.Embed(title="Человек не в голосовом канале",
                                  description="")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        try:
            unverify = interaction.guild.get_role(Roles.unverify)
            await member.remove_roles(unverify)
        except:
            pass
        role = interaction.guild.get_role(Roles.boy)
        await member.add_roles(role)
        await interaction.message.edit(view=None)
        embed = disnake.Embed(title=f"{member} был верифицирован валидатором {interaction.user}",
                              description="")
        await interaction.response.send_message(embed=embed)
        try:
            mEmbed = disnake.Embed(title=f"Валидатор {interaction.user} верифицировал тебя",
                                   description="Пожалуйста, оцените его работу ниже по 5-ти балльной шкале\n"
                                               "Приятного времяпрепровождения на нашем сервере!")
            await member.send(embed=mEmbed, view=RateView(user=member, validator=interaction.user))
        except:
            pass


class RejectButton(disnake.ui.Button):
    def __init__(self, user):
        super().__init__(style=disnake.ButtonStyle.red, label="Отклонить", custom_id="reject")
        self.user = user

    async def callback(self, interaction):
        member = interaction.guild.get_member(self.user.id)
        staff = interaction.guild.get_role(Staff.validator)
        if staff not in interaction.user.roles:
            embed = disnake.Embed(title="Недостаточно прав",
                                  description="")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        verify_chs = [interaction.guild.get_channel(i) for i in Channels.verify]
        member_in_voice = False
        for ch in verify_chs:
            if member in ch.members:
                member_in_voice = True
        if not member_in_voice:
            embed = disnake.Embed(title="Человек не в голосовом канале",
                                  description="")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        embed = disnake.Embed(title=f"{member} был(а) недопущен(а) валидатором {interaction.user}",
                              description="")
        await interaction.response.send_message(embed=embed)
        try:
            mEmbed = disnake.Embed(title=f"Валидатор {interaction.user} недопустил тебя",
                                   description="Подать заявку на апелляцию ты можешь в канале `『📃』appeal`")
            await member.send(embed=mEmbed)
        except:
            pass
        unverify = interaction.guild.get_role(Roles.unverify)
        await member.remove_roles(unverify)
        localban_role = interaction.guild.get_role(Roles.localban)
        await member.add_roles(localban_role)
        await interaction.message.edit(view=None)

        if DataBase.localban.count_documents({"_id": member.id}) == 0:
            post = {
                "_id": member.id,
                "name": member.name,
                "localban": True,
                "issued_by": interaction.author.id,
                "timestamp": interaction.created_at.strftime(System.date_format)
            }
            DataBase.localban.insert_one(post)


class VerifyView(disnake.ui.View):
    def __init__(self, user):
        super().__init__(timeout=None)
        self.add_item(GirlButton(user))
        self.add_item(BoyButton(user))
        self.add_item(RejectButton(user))


class Rate_1(disnake.ui.Button):
    def __init__(self, user, validator):
        super().__init__(style=disnake.ButtonStyle.red, label="1", custom_id="r1")
        self.user = user
        self.validator = validator

    async def callback(self, interaction):
        validator = self.validator
        guild = interaction.bot.get_guild(Guild.guild)
        member = guild.get_member(self.user.id)
        post = {
            "_id": self.validator.id,
            "name": self.validator.name,
            "rating": 1,
            "rates": [1]
        }

        await interaction.message.edit(view=None)
        if DataBase.validators.count_documents({"_id": validator.id}) == 0:
            DataBase.validators.insert_one(post)
        else:
            DataBase.validators.update_one({"_id": validator.id}, {"$push": {"rates": 1}})
            DataBase.validators.update_one({"_id": validator.id}, {
                "$set": {"rating": sum(i for i in DataBase.validators.find_one({"_id": validator.id})["rates"])}})

        embed = disnake.Embed(title=f"Спасибо за вашу оценку!",
                              description="Надеемся, что вы оценивали справедливо :)")
        await member.send(embed=embed)


class Rate_2(disnake.ui.Button):
    def __init__(self, user, validator):
        super().__init__(style=disnake.ButtonStyle.red, label="2", custom_id="r2")
        self.user = user
        self.validator = validator

    async def callback(self, interaction):
        validator = self.validator
        guild = interaction.bot.get_guild(Guild.guild)
        member = guild.get_member(self.user.id)
        post = {
            "_id": self.validator.id,
            "name": self.validator.name,
            "rating": 2,
            "rates": [2]
        }

        await interaction.message.edit(view=None)
        if DataBase.validators.count_documents({"_id": validator.id}) == 0:
            DataBase.validators.insert_one(post)
        else:
            DataBase.validators.update_one({"_id": validator.id}, {"$push": {"rates": 2}})
            DataBase.validators.update_one({"_id": validator.id}, {
                "$set": {"rating": sum(i for i in DataBase.validators.find_one({"_id": validator.id})["rates"])}})

        embed = disnake.Embed(title=f"Спасибо за вашу оценку!",
                              description="Надеемся, что вы оценивали справедливо :)")
        await member.send(embed=embed)


class Rate_3(disnake.ui.Button):
    def __init__(self, user, validator):
        super().__init__(style=disnake.ButtonStyle.blurple, label="3", custom_id="r3")
        self.user = user
        self.validator = validator

    async def callback(self, interaction):
        validator = self.validator
        guild = interaction.bot.get_guild(Guild.guild)
        member = guild.get_member(self.user.id)
        post = {
            "_id": self.validator.id,
            "name": self.validator.name,
            "rating": 3,
            "rates": [3]
        }

        await interaction.message.edit(view=None)
        if DataBase.validators.count_documents({"_id": validator.id}) == 0:
            DataBase.validators.insert_one(post)
        else:
            DataBase.validators.update_one({"_id": validator.id}, {"$push": {"rates": 3}})
            DataBase.validators.update_one({"_id": validator.id}, {
                "$set": {"rating": sum(i for i in DataBase.validators.find_one({"_id": validator.id})["rates"])}})

        embed = disnake.Embed(title=f"Спасибо за вашу оценку!",
                              description="Надеемся, что вы оценивали справедливо :)")
        await member.send(embed=embed)


class Rate_4(disnake.ui.Button):
    def __init__(self, user, validator):
        super().__init__(style=disnake.ButtonStyle.green, label="4", custom_id="r4")
        self.user = user
        self.validator = validator

    async def callback(self, interaction):
        validator = self.validator
        guild = interaction.bot.get_guild(Guild.guild)
        member = guild.get_member(self.user.id)
        post = {
            "_id": self.validator.id,
            "name": self.validator.name,
            "rating": 4,
            "rates": [4]
        }

        await interaction.message.edit(view=None)
        if DataBase.validators.count_documents({"_id": validator.id}) == 0:
            DataBase.validators.insert_one(post)
        else:
            DataBase.validators.update_one({"_id": validator.id}, {"$push": {"rates": 4}})
            DataBase.validators.update_one({"_id": validator.id}, {
                "$set": {"rating": sum(i for i in DataBase.validators.find_one({"_id": validator.id})["rates"])}})

        embed = disnake.Embed(title=f"Спасибо за вашу оценку!",
                              description="Надеемся, что вы оценивали справедливо :)")
        await member.send(embed=embed)


class Rate_5(disnake.ui.Button):
    def __init__(self, user, validator):
        super().__init__(style=disnake.ButtonStyle.green, label="5", custom_id="r5")
        self.user = user
        self.validator = validator

    async def callback(self, interaction):
        validator = self.validator
        guild = interaction.bot.get_guild(Guild.guild)
        member = guild.get_member(self.user.id)
        post = {
            "_id": self.validator.id,
            "name": self.validator.name,
            "rating": 5,
            "rates": [5]
        }

        await interaction.message.edit(view=None)
        if DataBase.validators.count_documents({"_id": validator.id}) == 0:
            DataBase.validators.insert_one(post)
        else:
            DataBase.validators.update_one({"_id": validator.id}, {"$push": {"rates": 5}})
            DataBase.validators.update_one({"_id": validator.id}, {
                "$set": {"rating": sum(i for i in DataBase.validators.find_one({"_id": validator.id})["rates"])}})

        embed = disnake.Embed(title=f"Спасибо за вашу оценку!",
                              description="Надеемся, что вы оценивали справедливо :)")
        await member.send(embed=embed)


class RateView(disnake.ui.View):
    def __init__(self, user, validator):
        super().__init__(timeout=None)
        self.add_item(Rate_1(user, validator))
        self.add_item(Rate_2(user, validator))
        self.add_item(Rate_3(user, validator))
        self.add_item(Rate_4(user, validator))
        self.add_item(Rate_5(user, validator))


class Verification(commands.Cog, name='Verification'):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member):
        rules_channel = self.bot.get_channel(1054280833361514589)
        staff_channel = self.bot.get_channel(Channels.verification)
        staff = member.guild.get_role(Staff.validator)
        try:
            unverify = member.guild.get_role(Roles.unverify)
            localban_role = member.guild.get_role(Roles.localban)
            if DataBase.localban.count_documents({"_id": member.id}) == 0:
                await member.add_roles(unverify)
            else:
                await member.add_roles(localban_role)
        except:
            pass

        'EMBED'
        embed = disnake.Embed(title="Новый пользователь",
                              description=f"{member.mention} присоединился к серверу.")
        embed.add_field(name="Ник",
                        value=member,
                        inline=True)
        embed.add_field(name="ID",
                        value=member.id,
                        inline=True)
        embed.add_field(name="Зарегистрирован:",
                        value=member.created_at.strftime(System.date_format),
                        inline=True)
        try:
            embed.set_thumbnail(
                url=member.avatar.url)
        except:
            pass

        'DM_EMBED'
        dm_embed = disnake.Embed(title="Добро пожаловать на HappyServer!",
                                 description=f"{member.name}, на данный момент вы **не верефицированный** пользователь.\n"
                                             f"Чтобы пройти верификацию, зайдите в один из каналов `verify`, где к вам подойдёт *Валидатор*.\n"
                                             f"Так же рекомендуется ознакомиться с {rules_channel.mention} нашего сервера, ведь ***не знание правил не освобождает от ответственности***!")

        if DataBase.localban.count_documents({"_id": member.id}) == 0:
            try:
                await member.send(embed=dm_embed)
            except:
                pass
            ment = await staff_channel.send(content=f"НОВЫЙ ПОЛЬЗОВАТЕЛЬ {staff.mention}",
                                            delete_after=0)
            msg = await staff_channel.send(embed=embed,
                                           view=VerifyView(user=member))


def setup(bot):
    bot.add_cog(Verification(bot))
