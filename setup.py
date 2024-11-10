import os
import platform
import random
import time
import traceback

import disnake
from disnake.ext import commands, tasks

from cogs.variables import bot, config, logger


class Check(commands.Bot):
    def __init__(self):
        self.loaded = False
        super().__init__()


if __name__ == '__main__':
    check = Check()


@bot.event
async def on_ready() -> None:
    if check.loaded:
        logger.info('ParaDoxBot переподключился')
    else:
        logger.info(f"DISNAKE: {disnake.__version__}")
        logger.info(f"PYTHON: {platform.python_version()}")
        logger.info(f"OS: {platform.system()} {platform.release()} ({os.name})")
        logger.debug("Установка расширений...")
        await load_cogs()
        logger.debug("Загрузка расширений завершена!\n")
        logger.debug("Запуск цикла статуса...")
        status_task.start()
        logger.debug("Цикл статуса успешно запущен!\n")


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
                        logger.error(f"[EXT] Произошла ошибка при попытке выгрузить расширение {exception}")

                    try:
                        bot.load_extension(f"cogs.{extension}")
                        ext_end = time.time()
                        logger.bebug(
                            f"[EXT] расширение {extension} успешно перезагружено ({(ext_end - ext_start) * 1000:.2f}мс)")
                        embed = disnake.Embed(title=f"Расширение {extension} перезагружено",
                                              description="")
                        await interaction.send(embed=embed, delete_after=10.0)
                    except Exception as e:
                        exception = f"{type(e).__name__}: {e}."
                        logger.error(f"[EXT] Произошла ошибка при попытке загрузить расширение {exception}")
                        embed = disnake.Embed(title=f"Расширение {extension} не удалось перезагрузить",
                                              description=f"{exception}")
                        await interaction.followup.send(embed=embed)
        else:
            try:
                ext_start = time.time()
                bot.unload_extension(f"cogs.{name}")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}."
                logger.error(f"[EXT] Произошла ошибка при попытке выгрузить расширение {exception}")

            try:
                bot.load_extension(f"cogs.{name}")
                ext_end = time.time()
                logger.debug(f"[EXT] расширение {name} успешно перезагружено ({(ext_end - ext_start) * 1000:.2f}мс)")
                embed = disnake.Embed(title=f"Расширение {name} перезагружено",
                                      description="")
                await interaction.followup.send(embed=embed)
            except Exception as e:
                exception = f"{type(e).__name__}: {e}."
                logger.error(f"[EXT] Произошла ошибка при попытке загрузить расширение {exception}")
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
            logger.debug(f"[EXT] расширение {name} успешно загружено ({(ext_end - ext_start) * 1000:.2f}мс)")
            embed = disnake.Embed(title=f"Расширение {name} загружено",
                                  description="")
            await interaction.followup.send(embed=embed)
        except Exception as e:
            exception = f"{type(e).__name__}: {e}."
            logger.error(f"[EXT] Произошла ошибка при попытке загрузить расширение {exception}")
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
            logger.debug(f"[EXT] расширение {name} успешно выгружено ({(ext_end - ext_start) * 1000:.2f}мс)")
            embed = disnake.Embed(title=f"Расширение {name} выгружено",
                                  description="")
            await interaction.followup.send(embed=embed)
        except Exception as e:
            exception = f"{type(e).__name__}: {e}."
            logger.error(f"[EXT] Произошла ошибка при попытке выгрузить расширение {exception}")
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
                logger.debug(f"[EXT] расширение {extension} успешно загружено ({(ext_end - ext_start) * 1000:.2f}мс)")
            except Exception as e:
                exception = (f"{type(e).__name__}: {e}.\n"
                             f"{traceback.format_exc()}")
                logger.error(f"[EXT] Произошла ошибка при попытке загрузить расширение {exception}")


bot.run(config["token"])
