import json
from sys import stdout
from logging import Logger, INFO, Formatter, StreamHandler
from logging.handlers import TimedRotatingFileHandler
from os import path, listdir, getcwd
from typing import Annotated

from coloredlogs import install

from interactions import Client, MISSING, global_autocomplete, AutocompleteContext, SlashCommandChoice
from pyclasher import PyClasherClient, ClanRequest, ClanSearchRequest, PlayerRequest
from pyclasher.models import ApiCodes, Clan

from Database.Database import DataBase
from Database.user import User
from Bot.Converters.PyClasher import PlayerConverter, ClanConverter


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
            log_name: str = "HeadHunterBot",
            log_level: int = INFO,
            log_file: str = "HeadhunterBot.log",
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
            self.cfg: dict = json.load(config_json)['headhunter_bot']

        super().__init__(
            token=self.cfg['discord_token'],
            logger=HeadhunterLogger(self.cfg['log_folder_path']),
            sync_ext=True,
            debug_scope=self.cfg['debug_scope'] or MISSING
        )

        self.cwd = getcwd()
        self.pyclasher_client = PyClasherClient(
            self.cfg['clash_of_clans_tokens'],
            requests_per_second=5
        )
        self.db = DataBase(self.cfg['db_path'], self.cfg['db_name'], self.logger)
        self.db_user = User()

        return

    async def astart(self, token: str | None = None) -> None:
        self.pyclasher_client.start()
        await super().astart(token)
        return

    async def stop(self) -> None:
        await super().stop()
        await self.pyclasher_client.close()
        return

    def get_extension_names(self) -> list[str]:
        filenames = listdir(path.join(self.cwd, "Bot", "Extensions"))

        return [".".join(("Bot", "Extensions", filename[:-3])) for filename in filenames if filename[0].isupper() and filename[-3:] == ".py"]

    def load_extensions(self) -> None:
        for file in self.get_extension_names():
            self.load_extension(file)
        return

    def load_extension(self, name: str, package: str = None) -> None:
        self.logger.info(f"Loading '{name}'.")
        super().load_extension(name, package)
        return

    def reload_extensions(self) -> None:
        for file in self.get_extension_names():
            self.reload_extension(file)
        return

    def reload_extension(self, name: str) -> None:
        self.logger.info(f"Reloading {name}.")
        super().reload_extension(name)
        return

    @global_autocomplete(option_name="clan")
    async def clan_autocomplete(self, ctx: AutocompleteContext, clans: Annotated[list[ClanRequest], ClanConverter]) -> None:
        if clans is None:
            await ctx.send([])
            return

        requests: list[ClanRequest] = []

        for clan in clans:
            try:
                req = await clan.request()
            except ApiCodes.NOT_FOUND:
                pass
            else:
                requests.append(req)

        await ctx.send(
            SlashCommandChoice(
                name=f"members: {clan.members}/50"
                     f"languate: {clan.chat_language}"
                     f"location: {clan.location}"
                     f"tag: {clan.tag}",
                value=clan.tag) for clan in requests[:25]
        )
        return

    @global_autocomplete(option_name="player")
    async def player_autocomplete(self, ctx: AutocompleteContext, players: Annotated[list[PlayerRequest], PlayerConverter]) -> None:
        if players is None:
            await ctx.send([])
            return

        requests: list[PlayerRequest] = []

        for player in players:
            try:
                req = await player.request()
            except ApiCodes.NOT_FOUND:
                pass
            else:
                requests.append(req)

        await ctx.send(
            SlashCommandChoice(
                name=f"tag: {player.tag}, "
                     f"clan: {player.clan.name}, "
                     f"level: {player.exp_level}, "
                     f"town hall: {player.town_hall_level}",
                value=player.tag) for player in requests
        )
        return
