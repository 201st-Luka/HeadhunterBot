# IMPORTS -----------------------------------------------------------------------------------------
# modules -----------------------------------------------------------------------------------------
import interactions
import logging
import coloredlogs


# scripts -----------------------------------------------------------------------------------------
from Bot.Variables import log, discordApiToken
from Database.Data_base import DataBase
from Database.User import User


# LOGGING -----------------------------------------------------------------------------------------
logger = logging.getLogger()
# log.setLevel(logging.DEBUG)

output_file_handler = logging.FileHandler(log)
output_file_handler.setFormatter(logging.Formatter("[%(asctime)s]:\t[%(levelname)s]:\t[%(name)s]:\t%(message)s"))

console_handler = logging.StreamHandler(print())
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter("[%(asctime)s]:\t[%(levelname)s]:\t[%(name)s]:\t%(message)s"))

logger.addHandler(output_file_handler)
logger.addHandler(console_handler)

coloredlogs.install(level=logging.INFO, logger=logger)


# DATABASE ----------------------------------------------------------------------------------------
db = DataBase()
user = User(db)


# GUILD MANAGEMENT --------------------------------------------------------------------------------
guildIdList = user.guilds.fetch_guild_ids()
# guildIdList = (893218147740565524)


# BOT ---------------------------------------------------------------------------------------------
headhunterBot = interactions.Client(
    token=discordApiToken,
    default_scope=guildIdList
)

headhunterBot.load("Bot.Extensions.Events", user=user, logger=logger)
headhunterBot.load("Bot.Extensions.activity", user=user)
headhunterBot.load("Bot.Extensions.botcommands")
headhunterBot.load("Bot.Extensions.clan", user=user)
headhunterBot.load("Bot.Extensions.player", user=user)
headhunterBot.load("Bot.Extensions.PrivateCommands")
headhunterBot.load("Bot.Extensions.sudo", user=user)


# BOT START ---------------------------------------------------------------------------------------
headhunterBot.start()


# BOT STOP ----------------------------------------------------------------------------------------
db.close()


# weitliegende statistiken (detailliert) -> evt visualisierung mit math plot lib
#
