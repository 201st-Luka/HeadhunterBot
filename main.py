# IMPORTS -----------------------------------------------------------------------------------------
# modules -----------------------------------------------------------------------------------------
import interactions
import logging
import coloredlogs


# scripts -----------------------------------------------------------------------------------------
from Bot.Variables import log, discordApiToken
from Bot.Extensions.Extensionssetup import setup
from Bot.Databaseinstance import DbInstance


# LOGGING -----------------------------------------------------------------------------------------
Log = logging.getLogger()
# log.setLevel(logging.DEBUG)

output_file_handler = logging.FileHandler(log)
output_file_handler.setFormatter(logging.Formatter("[%(asctime)s]:\t[%(levelname)s]:\t[%(name)s]:\t%(message)s"))

console_handler = logging.StreamHandler(print())
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter("[%(asctime)s]:\t[%(levelname)s]:\t[%(name)s]:\t%(message)s"))

Log.addHandler(output_file_handler)
Log.addHandler(console_handler)

coloredlogs.install(level=logging.INFO, logger=Log)


# DATABASE ----------------------------------------------------------------------------------------
db_instance = DbInstance()
user = db_instance.user

# GUILD MANAGEMENT --------------------------------------------------------------------------------
guildIdList = user.guilds.fetch_guild_ids()
# guildIdList = (893218147740565524)


def get_clan_tag_for_guild(guild_id):
    return user.guilds.fetch_clantag(guild_id)


# BOT ---------------------------------------------------------------------------------------------
headhunterBot = interactions.Client(
    token=discordApiToken,
    default_scope=guildIdList,
    disable_sync=False
)


setup(headhunterBot)


# BOT START ---------------------------------------------------------------------------------------
headhunterBot.start()

# BOT STOP ----------------------------------------------------------------------------------------
db_instance.close_db()


# weitliegende statistiken (detailliert) -> evt visualisierung mit math plot lib
#
