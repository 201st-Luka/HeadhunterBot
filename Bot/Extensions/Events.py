from interactions import Extension, listen, Status, Activity, ActivityType
from interactions.api.events import CommandError, Ready, Startup, AutocompleteError

from Bot.Exceptions import HeadhunterException
from Bot.HeadhunterBot import HeadhunterClient


class Events(Extension):

    def __init__(self, client: HeadhunterClient):
        self.client = client

    @listen(Ready)
    async def on_ready(self, event: Ready) -> None:
        self.client.logger.info(f"Logging in as {self.bot.user.username} ({self.bot.user.id})")
        guilds_bot_is_on = self.client.guilds
        guild_ids = self.client.db_user.guilds.fetch_guild_ids()
        for guild in guilds_bot_is_on:
            if guild.id not in guild_ids:
                self.client.db_user.guilds.insert_guild(guild.id, guild_name=str(guild.name))
        self.client.logger.info(f"Successfully logged in.")

    @listen(Startup)
    async def on_startup(self, event: Startup) -> None:
        await self.client.change_presence(
            status=Status.ONLINE,
            activity=Activity(
                name="in development...",
                type=ActivityType.GAME
            )
        )
        self.client.logger.info("The bot started.")

    @listen(CommandError)
    async def on_command_error(self, event: CommandError) -> None:
        if event.ctx.responded:
            return
        if isinstance(event.error, HeadhunterException):
            await event.ctx.send(str(event.error), ephemeral=True)
        else:
            await event.ctx.send(
                f"Something went wrong. Please report this error on my Discord server (`/dc`). Exception:\n```"
                f"diff\n- {str(event.error)}```", ephemeral=True)
            raise event.error

    @listen(AutocompleteError)
    async def on_autocomplete_error(self, event: AutocompleteError) -> None:
        if isinstance(event.error, HeadhunterException):
            await event.ctx.send([])
            return
        await event.ctx.send([])
        raise event.error


def setup(client: HeadhunterClient) -> None:
    Events(client)
