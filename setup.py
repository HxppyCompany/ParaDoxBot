import json
import os
import platform
import random
import sys
import time
import traceback

import disnake
from disnake import Intents
from disnake.ext import commands, tasks
from disnake.ext.commands import Bot

from pymongo.mongo_client import MongoClient

if not os.path.isfile("config.json"):
    sys.exit("Файл 'config.json' не обнаружен или повреждён!")
else:
    with open("config.json") as file:
        config = json.load(file)

database = MongoClient(config["mongodb"])

intents = Intents.all()
bot = Bot(
    command_prefix=commands.when_mentioned_or(config["prefix"]),
    intents=intents)
bot.config = config


class Check(commands.Bot):
    def __init__(self):
        self.loaded = False
        super().__init__()


if __name__ == '__main__':
    check = Check()


@bot.event
async def on_ready() -> None:
    if check.loaded:
        print('╔═══════════INFO═══════════╗')
        print("║ HappyBot переподключился ║")
        print("╚══════════════════════════╝")
    else:
        print("╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░║")
        print("║░░░░░░██╗░░██╗░█████╗░██████╗░██████╗░██╗░░░██╗██████╗░░█████╗░████████╗░░░░░░║")
        print("║░░░░░░██║░░██║██╔══██╗██╔══██╗██╔══██╗╚██╗░██╔╝██╔══██╗██╔══██╗╚══██╔══╝░░░░░░║")
        print("║░░░░░░███████║███████║██████╔╝██████╔╝░╚████╔╝░██████╦╝██║░░██║░░░██║░░░░░░░░░║")
        print("║░░░░░░██╔══██║██╔══██║██╔═══╝░██╔═══╝░░░╚██╔╝░░██╔══██╗██║░░██║░░░██║░░░░░░░░░║")
        print("║░░░░░░██║░░██║██║░░██║██║░░░░░██║░░░░░░░░██║░░░██████╦╝╚█████╔╝░░░██║░░░░░░░░░║")
        print("║░░░░░░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░░░░╚═╝░░░░░░░░╚═╝░░░╚═════╝░░╚════╝░░░░╚═╝░░░░░░░░░║")
        print("║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░║")
        print("║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░║")
        print("║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▄▄░█▄█░░░█░█░▄▀█░█▀█░█▀█░█▄█░█▀▀░▄▀█░█▄░█░░║")
        print("║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▄█░░█░░░░█▀█░█▀█░█▀▀░█▀▀░░█░░█▀░░█▀█░█░▀█░░║")
        print("║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░║")
        print("╠══════════════════════════════════════════════════════════════════════════════╣")
        print(f"║ DISNAKE: {disnake.__version__}")
        print(f"║ PYTHON: {platform.python_version()}")
        print(f"║ OS: {platform.system()} {platform.release()} ({os.name})")
        print("╚══════════════════════════════════════════════════════════════════════════════╝")
        print("Установка расширений...")
        await load_cogs()
        print("Загрузка расширений завершена!")
        print("-------------------")
        print("Подключаюсь к MongoDB...")
        try:
            database.admin.command('ping')
            print(f"[MBD] Соединение установлено!")
        except Exception as e:
            print(f"[MDB]|[ERROR] Ошибка при попытке обращения к MongoDB: {e}.")
        print("-------------------")
        print("Запуск цикла статуса...")
        status_task.start()
        print("Цикл статуса успешно запущен!")
        print("-------------------")


@tasks.loop(minutes=10)
async def status_task() -> None:
    statuses = ["очке пальчиком", "анальчике твоего отчима", "твоей маме", "Minecraft", "дилдо", "Terraria",
                f"Python {platform.python_version()}", f"Disnake {disnake.__version__}", "PyCharm Professional",
                "Console", "симулятор человека", "баги и ошибки", "pip 32.0"]
    await bot.change_presence(activity=disnake.Game(random.choice(statuses)))


@bot.slash_command(
    name="reload",
    description="Разгружает расширения",
    default_member_permissions=disnake.Permissions(administrator=True),
    options=[
        disnake.Option(
            name="name",
            description="Название расширения",
            type=disnake.OptionType.string,
            required=True
        )
    ]
)
async def reload(interaction, name):
    ext_start = 0

    await interaction.response.defer(ephemeral=True)
    if interaction.author.id in config["owners"]:
        if name == "all":
            for filename in os.listdir(f"./cogs"):
                if filename.endswith(".py"):
                    extension = filename[:-3]
                    try:
                        ext_start = time.time()
                        bot.unload_extension(f"cogs.{extension}")
                    except Exception as e:
                        exception = f"{type(e).__name__}: {e}."
                        print(f"[EXT]|[ERROR] Произошла ошибка при попытке выгрузить расширение {exception}")

                    try:
                        bot.load_extension(f"cogs.{extension}")
                        ext_end = time.time()
                        print(
                            f"[EXT] расширение {extension} успешно перезагружено ({(ext_end - ext_start) * 1000:.2f}мс)")
                        embed = disnake.Embed(title=f"Расширение {extension} перезагружено",
                                              description="")
                        await interaction.send(embed=embed, delete_after=10.0)
                    except Exception as e:
                        exception = f"{type(e).__name__}: {e}."
                        print(f"[EXT]|[ERROR] Произошла ошибка при попытке загрузить расширение {exception}")
                        embed = disnake.Embed(title=f"Расширение {extension} не удалось перезагрузить",
                                              description=f"{exception}")
                        await interaction.followup.send(embed=embed)
        else:
            try:
                ext_start = time.time()
                bot.unload_extension(f"cogs.{name}")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}."
                print(f"[EXT]|[ERROR] Произошла ошибка при попытке выгрузить расширение {exception}")

            try:
                bot.load_extension(f"cogs.{name}")
                ext_end = time.time()
                print(f"[EXT] расширение {name} успешно перезагружено ({(ext_end - ext_start) * 1000:.2f}мс)")
                embed = disnake.Embed(title=f"Расширение {name} перезагружено",
                                      description="")
                await interaction.followup.send(embed=embed)
            except Exception as e:
                exception = f"{type(e).__name__}: {e}."
                print(f"[EXT]|[ERROR] Произошла ошибка при попытке загрузить расширение {exception}")
                embed = disnake.Embed(title=f"Расширение {name} не удалось перезагрузить",
                                      description=f"{exception}")
                await interaction.followup.send(embed=embed)


@bot.slash_command(
    name="load",
    description="Загружает расширения",
    default_member_permissions=disnake.Permissions(administrator=True),
    options=[
        disnake.Option(
            name="name",
            description="Название расширения",
            type=disnake.OptionType.string,
            required=True
        )
    ]
)
async def load(interaction, name):
    await interaction.response.defer(ephemeral=True)
    if interaction.author.id in config["owners"]:
        try:
            ext_start = time.time()
            bot.load_extension(f"cogs.{name}")
            ext_end = time.time()
            print(f"[EXT] расширение {name} успешно загружено ({(ext_end - ext_start) * 1000:.2f}мс)")
            embed = disnake.Embed(title=f"Расширение {name} загружено",
                                  description="")
            await interaction.followup.send(embed=embed)
        except Exception as e:
            exception = f"{type(e).__name__}: {e}."
            print(f"[EXT]|[ERROR] Произошла ошибка при попытке загрузить расширение {exception}")
            embed = disnake.Embed(title=f"Расширение {name} не удалось загрузить",
                                  description=f"{exception}")
            await interaction.followup.send(embed=embed)


@bot.slash_command(
    name="unload",
    description="Выгружает расширения",
    default_member_permissions=disnake.Permissions(administrator=True),
    options=[
        disnake.Option(
            name="name",
            description="Название расширения",
            type=disnake.OptionType.string,
            required=True
        )
    ]
)
async def unload(interaction, name):
    await interaction.response.defer(ephemeral=True)
    if interaction.author.id in config["owners"]:
        await interaction.message.delete()
        try:
            ext_start = time.time()
            bot.unload_extension(f"cogs.{name}")
            ext_end = time.time()
            print(f"[EXT] расширение {name} успешно выгружено ({(ext_end - ext_start) * 1000:.2f}мс)")
            embed = disnake.Embed(title=f"Расширение {name} выгружено",
                                  description="")
            await interaction.followup.send(embed=embed)
        except Exception as e:
            exception = f"{type(e).__name__}: {e}."
            print(f"[EXT]|[ERROR] Произошла ошибка при попытке выгрузить расширение {exception}")
            embed = disnake.Embed(title=f"Расширение {name} не удалось загрузить",
                                  description=f"{exception}")
            await interaction.followup.send(embed=embed)


async def load_cogs() -> None:
    for filename in os.listdir(f"./cogs"):
        if filename.endswith(".py"):
            extension = filename[:-3]
            try:
                ext_start = time.time()
                bot.load_extension(f"cogs.{extension}")
                ext_end = time.time()
                print(f"[EXT] расширение {extension} успешно загружено ({(ext_end - ext_start) * 1000:.2f}мс)")
            except Exception as e:
                exception = (f"{type(e).__name__}: {e}.\n"
                             f"{traceback.format_exc()}")
                print(f"[EXT]|[ERROR] Произошла ошибка при попытке загрузить расширение {exception}")


bot.run(config["token"])
