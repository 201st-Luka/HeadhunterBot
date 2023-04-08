import logging

import coloredlogs
import interactions

from Bot.variables import Variables
from Database.data_base import DataBase
from Database.user import User


class Main:
    def __init__(self):
        self.logger = logging.getLogger()
        self.variables = Variables()
        self.configure_logging(self.variables.log_file_name, log_level=logging.INFO)
        self.db = DataBase()
        self.user = User(self.db)
        self.guild_id_list = self.user.guilds.fetch_guild_ids()
        self.bot = None

    def configure_logging(self, log_file, log_level=logging.INFO):
        self.logger.setLevel(log_level)

        output_file_handler = logging.FileHandler(log_file)
        output_file_handler.setFormatter(
            logging.Formatter("[%(asctime)s]:\t[%(levelname)s]:\t[%(name)s]:\t%(message)s"))

        console_handler = logging.StreamHandler(print())
        console_handler.setLevel(log_level)
        console_handler.setFormatter(logging.Formatter("[%(asctime)s]:\t[%(levelname)s]:\t[%(name)s]:\t%(message)s"))

        self.logger.addHandler(output_file_handler)
        self.logger.addHandler(console_handler)

        coloredlogs.install(level=log_level, logger=self.logger)

    def start_bot(self):
        self.bot = interactions.Client(token=self.variables.discord_api_token, default_scope=self.guild_id_list)

        self.bot.load(f"Bot.Extensions.events", user=self.user, logger=self.logger)
        self.bot.load(f"Bot.Extensions.activity", user=self.user)
        self.bot.load(f"Bot.Extensions.bot_commands")
        self.bot.load(f"Bot.Extensions.clan", user=self.user)
        self.bot.load(f"Bot.Extensions.player", user=self.user)
        self.bot.load(f"Bot.Extensions.private_commands")
        self.bot.load(f"Bot.Extensions.sudo", user=self.user)

        self.bot.start()

    def stop_bot(self):
        self.db.close()


if __name__ == '__main__':
    bot = Main()
    bot.start_bot()
    bot.stop_bot()
