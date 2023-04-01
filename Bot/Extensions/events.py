from logging import Logger

from interactions import Extension, Client, extension_listener, ClientPresence, StatusType, PresenceActivity, \
    PresenceActivityType, CommandContext

from Bot.exceptions import NoClanTagLinked, NoPlayerTagLinked, InvalidPlayerTag, AlreadyLinkedClanTag, InvalidClanTag, \
    AlreadyLinkedPlayerTag
from Database.user import User


class Events(Extension):
    client: Client
    user: User
    logger: Logger

    def __init__(self, client: Client, user: User, logger: Logger):
        self.client = client
        self.user = user
        self.logger = logger

    @extension_listener(name="on_ready")
    async def on_ready(self) -> None:
        self.logger.info(f"Logging in as {self.client.me.name} ({self.client.me.id})")
        guilds_bot_is_on = self.client.guilds
        guild_ids = self.user.guilds.fetch_guild_ids()
        for guild in guilds_bot_is_on:
            if guild.id not in guild_ids:
                self.user.guilds.insert_guild(guild.id, guild_name=str(guild.name))
        self.logger.info(f"Successfully logged in.")

    @extension_listener(name="on_start")
    async def on_start(self) -> None:
        await self.client.change_presence(ClientPresence(
            status=StatusType.ONLINE,
            activities=[
                PresenceActivity(
                    name="in development...",
                    type=PresenceActivityType.GAME
                )
            ]
        ))
        self.logger.info("The bot started.")

    @extension_listener(name="on_command")
    async def on_command(self, ctx: CommandContext) -> None:
        self.logger.info(f"The user {ctx.user.username}#{ctx.user.discriminator} ({ctx.user.id}) "
                         f"used {ctx.command.name}.")

    @extension_listener(name="on_command_error")
    async def on_command_error(self, ctx: CommandContext, exception: Exception) -> None:
        match exception:
            case NoClanTagLinked():
                await ctx.send(
                    "This guild does not have a linked clan tag. Do `/sudo guild link_clan <clan tag>` first!")
            case InvalidClanTag():
                await ctx.send("Your entered clan tag is not valid!")
            case NoPlayerTagLinked():
                await ctx.send("You don't have a linked player tag. Do `/player link add <player tag>` first!")
            case InvalidPlayerTag():
                await ctx.send("Your entered player tag is not valid!")
            case AlreadyLinkedClanTag():
                await ctx.send("This clan has already been linked to this server.")
            case AlreadyLinkedPlayerTag():
                await ctx.send("This player has already been linked.")
            case _:
                await ctx.send(
                    f"Something went wrong. Please report this error on my Discord server (`/dc`). Exception:\n```diff\n- "
                    f"{str(exception)}```")
                self.logger.error(
                    f"An error occurred.\n{ctx.user.username}#{ctx.user.discriminator} ({ctx.user.id}) used {ctx.command.name} "
                    f"in the channel {ctx.channel.name} ({ctx.channel.id}) on guild {ctx.guild.name} ({ctx.guild.id}).\n"
                    f"Error: {ctx.command.error_callback}\n"
                    f"Exception: {exception}")
                raise exception


def setup(client: Client, user: User, logger: Logger) -> None:
    Events(client, user, logger)
