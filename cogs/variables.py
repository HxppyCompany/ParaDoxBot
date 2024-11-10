import datetime
import json
import os
import sys
import colorama

from disnake import Intents
from disnake.ext import commands
from disnake.ext.commands import Bot

from cogs.logger import Logger

__version__ = "0.1.0"

if not os.path.isfile("config.json"):
    sys.exit("Файл 'config.json' не обнаружен или повреждён!")
else:
    with open("config.json") as file:
        config = json.load(file)

intents = Intents.all()
bot = Bot(intents=intents)

owners = config['owners']

colorama.init()
fore = colorama.Fore
colors = {
    0: fore.RESET,
    1: fore.WHITE,
    2: fore.RED,
    3: fore.YELLOW,
    4: fore.GREEN,
    5: fore.CYAN,
    6: fore.BLUE,
    7: fore.MAGENTA,
    8: fore.BLACK,
    9: fore.LIGHTWHITE_EX,
    10: fore.LIGHTRED_EX,
    11: fore.LIGHTYELLOW_EX,
    12: fore.LIGHTGREEN_EX,
    13: fore.LIGHTCYAN_EX,
    14: fore.LIGHTBLUE_EX,
    15: fore.LIGHTMAGENTA_EX,
    16: fore.LIGHTBLACK_EX,
    'Reset': fore.RESET,
    'White': fore.WHITE,
    'Red': fore.RED,
    'Yellow': fore.YELLOW,
    'Green': fore.GREEN,
    'Cyan': fore.CYAN,
    'Blue': fore.BLUE,
    'Magenta': fore.MAGENTA,
    'Black': fore.BLACK,
    'WhiteEx': fore.LIGHTWHITE_EX,
    'RedEx': fore.LIGHTRED_EX,
    'YellowEx': fore.LIGHTYELLOW_EX,
    'GreenEx': fore.LIGHTGREEN_EX,
    'CyanEx': fore.LIGHTCYAN_EX,
    'BlueEx': fore.LIGHTBLUE_EX,
    'MagentaEx': fore.LIGHTMAGENTA_EX,
    'BlackEx': fore.LIGHTBLACK_EX
}

logger = Logger(
    level='info',
    strfmt=f"{colors[16]}<date> <level> {colors[9]}<message> {colors[16]}<module>",
    # datefmt="%H:%M:%S",
)


class System(commands.Cog):
    date_format = "%H:%M, %b %d, %Y"

    @staticmethod
    async def get_time(current_time):
        return current_time.astimezone(datetime.timezone(datetime.timedelta(hours=3))).strftime("%H:%M, %b %d, %Y")


class Guild(commands.Cog):
    guild = 1054280832862392430


class Roles(commands.Cog):
    unverify = 1091970906181619722
    girl = 1092494103289270352
    boy = 1092494271740903454
    localban = 1092551947871060100
    bot = 1092508778445951117
    staff = 1091972433545801772


class Staff(commands.Cog):
    validator = 1091970960900501524


class Channels(commands.Cog):
    verification = 1092003313823793243
    verify = [
        1092526320883351633
    ]
    vacancies = {
        'mod': 1092035406868004904,
        'validate': 1092035561088368681,
        'event': 1092035659847446549,
        'tribune': 1092035713932992662,
        'tester': 1092035849027334184
    }


class Images(commands.Cog):
    online = "https://happycompany.hb.ru-msk.vkcs.cloud/online.png"
    offline = "https://happycompany.hb.ru-msk.vkcs.cloud/offline.png"
    idle = "https://happycompany.hb.ru-msk.vkcs.cloud/idle.png"
    do_not_disturb = "https://happycompany.hb.ru-msk.vkcs.cloud/dnd.png"
    line = "https://happycompany.hb.ru-msk.vkcs.cloud/line.png"


def setup(bot):
    bot.add_cog(System(bot))
    bot.add_cog(Roles(bot))
    bot.add_cog(Staff(bot))
    bot.add_cog(Channels(bot))
