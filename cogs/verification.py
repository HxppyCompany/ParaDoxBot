import disnake
from disnake.ext import commands

from cogs.variables import System, logger
from cogs.variables import Roles
from cogs.variables import Staff
from cogs.variables import Channels


async def verify(self, role, interaction):
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

    await member.add_roles(role)
    await interaction.message.edit(view=None)
    embed = disnake.Embed(title=f"{member} был(а) верифицирован(а) саппортом {interaction.user}",
                          description="")
    await interaction.response.send_message(embed=embed)
    try:
        m_embed = disnake.Embed(title=f"Саппорт {interaction.user} верифицировал тебя",
                                description="Приятного времяпрепровождения на нашем сервере!")
        await member.send(embed=m_embed)
    except Exception as e:
        logger.error(f"{e}")


'''BUTTONS'''


class Y13Button(disnake.ui.Button):
    def __init__(self, user):
        super().__init__(style=disnake.ButtonStyle.blurple, label="13+", custom_id="verify13")
        self.user = user

    async def callback(self, interaction):
        role = interaction.guild.get_role(Roles.y13)
        await verify(self, role, interaction)


class Y15Button(disnake.ui.Button):
    def __init__(self, user):
        super().__init__(style=disnake.ButtonStyle.blurple, label="15+", custom_id="verify15")
        self.user = user

    async def callback(self, interaction):
        role = interaction.guild.get_role(Roles.y15)
        await verify(self, role, interaction)


class Y18Button(disnake.ui.Button):
    def __init__(self, user):
        super().__init__(style=disnake.ButtonStyle.blurple, label="18+", custom_id="verify18")
        self.user = user

    async def callback(self, interaction):
        role = interaction.guild.get_role(Roles.y18)
        await verify(self, role, interaction)


class Y20Button(disnake.ui.Button):
    def __init__(self, user):
        super().__init__(style=disnake.ButtonStyle.blurple, label="20+", custom_id="verify20")
        self.user = user

    async def callback(self, interaction):
        role = interaction.guild.get_role(Roles.y20)
        await verify(self, role, interaction)


class Y25Button(disnake.ui.Button):
    def __init__(self, user):
        super().__init__(style=disnake.ButtonStyle.blurple, label="25+", custom_id="verify25")
        self.user = user

    async def callback(self, interaction):
        role = interaction.guild.get_role(Roles.y25)
        await verify(self, role, interaction)


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
        embed = disnake.Embed(title=f"{member} был(а) недопущен(а) валидатором {interaction.user}",
                              description="")
        await interaction.response.send_message(embed=embed)
        try:
            m_embed = disnake.Embed(title=f"Валидатор {interaction.user} недопустил тебя",
                                    description="Подать заявку на апелляцию ты можешь в канале `『📃』appeal`")
            await member.send(embed=m_embed)
        except Exception as e:
            logger.error(f"{e}")
        unverify = interaction.guild.get_role(Roles.unverify)
        await member.remove_roles(unverify)
        localban_role = interaction.guild.get_role(Roles.localban)
        await member.add_roles(localban_role)
        await interaction.message.edit(view=None)


class VerifyView(disnake.ui.View):
    def __init__(self, user):
        super().__init__(timeout=None)
        self.add_item(Y13Button(user))
        self.add_item(Y15Button(user))
        self.add_item(Y18Button(user))
        self.add_item(Y20Button(user))
        self.add_item(Y25Button(user))
        self.add_item(RejectButton(user))


class Verification(commands.Cog, name='Verification'):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member):
        if member.bot:
            try:
                bot = member.guild.get_role(Roles.bot)
                return await member.add_roles(bot)
            except Exception as e:
                logger.error(f"{e}")
        rules_channel = self.bot.get_channel(1054280833361514589)
        staff_channel = self.bot.get_channel(Channels.verification)
        staff = member.guild.get_role(Staff.validator)
        try:
            unverify = member.guild.get_role(Roles.unverify)
            localban_role = member.guild.get_role(Roles.localban)
            await member.add_roles(unverify)
        except Exception as e:
            logger.error(f"{e}")

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
        except Exception as e:
            logger.error(f"{e}")

        'DM_EMBED'
        dm_embed = disnake.Embed(title="Добро пожаловать на HappyServer!",
                                 description=f"{member.name}, на данный момент вы "
                                             f"**не верефицированный** пользователь.\n"
                                             f"Чтобы пройти верификацию, зайдите в один из каналов `verify`, "
                                             f"где к вам подойдёт *Валидатор*.\n"
                                             f"Так же рекомендуется ознакомиться с {rules_channel.mention} "
                                             f"нашего сервера, ведь ***не знание правил не освобождает от "
                                             f"ответственности***!")

        try:
            await member.send(embed=dm_embed)
        except Exception as e:
            logger.error(f"{e}")
        await staff_channel.send(content=f"НОВЫЙ ПОЛЬЗОВАТЕЛЬ {staff.mention}",
                                 delete_after=0)
        await staff_channel.send(embed=embed,
                                 view=VerifyView(user=member))


def setup(bot):
    bot.add_cog(Verification(bot))
