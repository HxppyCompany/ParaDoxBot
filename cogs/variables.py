import json

from disnake.ext import commands

from pymongo.mongo_client import MongoClient

with open("config.json") as file:
    config = json.load(file)


class System(commands.Cog):
    date_format = "%b %d, %Y"


class DataBase(commands.Cog):
    database = MongoClient(config["mongodb"])
    users = database.USERS
    localban = users.localban
    validators = users.validators


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
        1092526320883351633,
        1092526425657069768,
        1092526469592391800,
        1092526548290129972,
        1092526577583128576
    ]


# class Templates(commands.Cog):


def setup(bot):
    bot.add_cog(System(bot))
    bot.add_cog(DataBase(bot))
    bot.add_cog(Roles(bot))
    bot.add_cog(Staff(bot))
    bot.add_cog(Channels(bot))
