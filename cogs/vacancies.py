import disnake
from disnake.ext import commands

from cogs.variables import Roles
from cogs.variables import Channels

'''BUTTONS'''


class ModalVacancies(disnake.ui.Modal):
    def __init__(self, arg, code):
        self.arg = arg
        self.code = code
        components = [
            disnake.ui.TextInput(
                label="Имя и Возраст", custom_id="name_age", placeholder="Ваше имя и возраст"
            ),
            disnake.ui.TextInput(
                label="Часовой пояс", custom_id="local_time", placeholder="Ваш часовой пояс"
            ),
            disnake.ui.TextInput(
                label="О себе", custom_id="about", style=disnake.TextInputStyle.long, placeholder="Расскажите о себе"
            ),
            disnake.ui.TextInput(
                label="Почему вы хотите встать на эту должность", custom_id="why", placeholder="Ответ"
            ),
            disnake.ui.TextInput(
                label="Рабочее время", custom_id="work_time", placeholder="Сколько вы готовы уделять времени серверу"
            )
        ]
        super().__init__(title=f"Заявка на {arg}", components=components, custom_id="vacanciesModal")

    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        name_age = interaction.text_values["name_age"]
        local_time = interaction.text_values["local_time"]
        about = interaction.text_values["about"]
        why = interaction.text_values["why"]
        work_time = interaction.text_values["work_time"]

        channel = interaction.guild.get_channel(Channels.vacancies[self.code])

        embed = disnake.Embed(title=f"Заявка от {interaction.user}",
                              description=f"Имя и возраст: {name_age}\n"
                                          f"Часовой пояс: {local_time}\n"
                                          f"О себе: {about}\n"
                                          f"Почему хочет стать: {why}\n"
                                          f"Рабочее время: {work_time}")

        await channel.send(embed=embed)

        await interaction.response.send_message(f"Заявка отправлена!", ephemeral=True)


class SelectVacancies(disnake.ui.Select):
    def __init__(self):
        options = [
            disnake.SelectOption(label="Модератор", value="mod"),
            disnake.SelectOption(label="Валидатор", value="valid"),
            disnake.SelectOption(label="Ивентер", value="event"),
            disnake.SelectOption(label="Трибунер", value="tribune"),
            disnake.SelectOption(label="Тестировщик", value="test")
        ]
        super().__init__(
            placeholder="Выбери одну из вакансий", options=options, min_values=0, max_values=1, custom_id="vacancies"
        )

    async def callback(self, interaction: disnake.MessageInteraction):
        if not interaction.values:
            await interaction.response.defer()
        elif Roles.staff in interaction.user.roles:
            embed = disnake.Embed(title=f"Стафф не может оставлять заявки!")
            await interaction.response.send_message(embed, ephemeral=True)
            return
        else:
            match code := interaction.values:
                case "mod":
                    await interaction.response.send_modal(ModalVacancies("Модератора", code))
                case "valid":
                    await interaction.response.send_modal(ModalVacancies("Валидатора", code))
                case "event":
                    await interaction.response.send_modal(ModalVacancies("Ивентера", code))
                case "tribune":
                    await interaction.response.send_modal(ModalVacancies("Трибунера", code))
                case "test":
                    await interaction.response.send_modal(ModalVacancies("Тестировщика", code))


class VacanciesView(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(SelectVacancies())


class Vacancies(commands.Cog, name="Vacancies"):
    def __init__(self, bot):
        self.bot = bot
        self.persistents_view_added = False

    @commands.slash_command(
        name="vacancies",
        description="",
        default_member_permissions=disnake.Permissions(administrator=True)
    )
    async def vacancies(self, interaction):
        await interaction.response.defer(ephemeral=True)
        embed = disnake.Embed(title="Доступные вакансии в staff",
                              description="Выбери одну из них ниже и заполни указанную форму!")

        view = disnake.ui.View()
        view.add_item(SelectVacancies())

        await interaction.followup.send(embed=embed, view=view)

    @commands.Cog.listener()
    async def on_connection(self):
        if self.persistents_view_added:
            return

        view = disnake.ui.View(timeout=None)
        view.add_item(SelectVacancies())
        self.bot.add_view(view, message_id=1129047565648801792)


def setup(bot):
    bot.add_cog(Vacancies(bot))
