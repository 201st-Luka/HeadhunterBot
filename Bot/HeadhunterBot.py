import json
from sys import stdout
from logging import Logger, INFO, Formatter, StreamHandler
from logging.handlers import TimedRotatingFileHandler
from os import path, listdir, getcwd
from coloredlogs import install

from interactions import Client, MISSING
from pyclasher import PyClasherClient


class HeadhunterLogger(Logger):
    log_format_str = "[%(asctime)s]:  [%(levelname)s]:  [%(name)s]:\t%(message)s"
    field_styles = {
        'asctime': {'color': 'green'},
        'hostname': {'color': 'magenta'},
        'levelname': {'bold': True, 'color': 'white'},
        'name': {'color': 'blue'},
        'programname': {'color': 'cyan'},
        'username': {'color': 'yellow'}
    }

    def __init__(
            self,
            log_path: str,
            log_name: str = "HeadHunterLog",
            log_level: int = INFO,
            log_file: str = "HeadhunterLog.log",
            log_file_suffix: str = "%Y_%m_%d"
    ):
        super().__init__(log_name, INFO)

        self.log_format = Formatter(self.log_format_str)

        output_file_handler = TimedRotatingFileHandler(
            filename=path.join(log_path, log_file),
            when="midnight",
            backupCount=14,
        )
        output_file_handler.suffix = log_file_suffix
        output_file_handler.setFormatter(
            self.log_format
        )

        console_handler = StreamHandler(stdout)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(self.log_format)

        self.addHandler(output_file_handler)
        self.addHandler(console_handler)

        install(
            level=log_level,
            logger=self,
            fmt=self.log_format_str,
            field_styles=self.field_styles
        )
        return


class HeadhunterClient(Client):
    def __init__(self, config: str) -> None:
        with open(config, "r") as config_json:
            self.cfg: dict = json.load(config_json)

        super().__init__(
            token=self.cfg['discord_token'],
            logger=HeadhunterLogger(self.cfg['log_folder_path']),
            sync_ext=True,
            debug_scope=self.cfg['debug_scope'] or MISSING
        )

        self.cwd = getcwd()
        self.pyclasher_client = PyClasherClient(self.cfg['tokens'])
        return

    async def astart(self, token: str | None = None) -> None:
        await self.pyclasher_client.start()

        await super().astart(token)

        return

    async def stop(self):
        await super().stop()
        await self.pyclasher_client.close()

        return

    def get_extension_names(self) -> list[str]:
        filenames = listdir(path.join(self.cwd, "Bot", "Extensions"))

        return [".".join(("Bot", "Extensions", filename[:-3])) for filename in filenames if filename[0].isupper()]

    def load_extensions(self):
        for file in self.get_extension_names():
            self.load_extension(file)
        return

    def load_extension(self, name: str, package: str = None):
        self.logger.info(f"Loading {name}.")
        super().load_extension(name, package)
        return

    def reload_extensions(self):
        for file in self.get_extension_names():
            self.reload_extension(file)
        return

    def reload_extension(self, name: str):
        self.logger.info(f"Reloading {name}.")
        super().reload_extension(name)
        return
