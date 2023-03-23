from logging import Logger

from interactions import Extension, Client, extension_listener, ClientPresence, StatusType, PresenceActivity, PresenceActivityType, CommandContext

from Bot.Exeptions import NoClanTagLinked, NoPlayerTagLinked, InvalidPlayerTag, AlreadyLinkedClanTag, InvalidClanTag
from Database.User import User


class Events(Extension):
    client: Client
    user: User
    logger: Logger

    def __init__(self, client: Client, user: User, logger: Logger):
        self.client = client
        self.user = user
        self.logger = logger
        return

    @extension_listener(name="on_start")
    async def on_start(self):
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
        return

    @extension_listener(name="on_ready")
    async def on_ready(self):
        self.logger.info(f"Logging in as {self.client.me.name} ({self.client.me.id})")
        guilds_bot_is_on = self.client.guilds
        guild_ids = self.user.guilds.fetch_guild_ids()
        for guild in guilds_bot_is_on:
            if guild.id not in guild_ids:
                self.user.guilds.insert_guild(guild.id, guild_name=str(guild.name))
        self.logger.info(f"Successfully logged in.")
        return

    @extension_listener(name="on_command")
    async def on_command(self, ctx: CommandContext):
        self.logger.info(f"The user {ctx.user.username}#{ctx.user.discriminator} ({ctx.user.id}) "
                         f"used {ctx.command.name}.")
        return

    @extension_listener(name="on_command_error")
    async def on_command_error(self, ctx: CommandContext, exception: Exception):
        match exception:
            case NoClanTagLinked():
                await ctx.send("This guild does not have a linked clan tag. Do `/sudo guild link_clan <clan tag>` first!")
                return
            case InvalidClanTag():
                await ctx.send("Your entered clan tag is not valid!")
                return
            case NoPlayerTagLinked():
                await ctx.send("You don't have a linked player tag. Do `/player link add <player tag>` first!")
                return
            case InvalidPlayerTag():
                await ctx.send("Your entered player tag is not valid!")
                return
            case AlreadyLinkedClanTag():
                await ctx.send("This clan has already been linked to this server")
                return
            case _:
                await ctx.send(
                    f"Something went wrong. Please report this error on my Discord server (`/dc`). Exception:\n```diff\n- "
                    f"{str(exception)}```")
                self.logger.error(f"An error occurred.\n{ctx.user.username}#{ctx.user.discriminator} ({ctx.user.id}) used {ctx.command.name} "
                                  f"in the channel {ctx.channel.name} ({ctx.channel.id}) on guild {ctx.guild.name} ({ctx.guild.id}). "
                                  f"Error: {ctx.command.error_callback}\nException: {exception}")
                raise exception


def setup(client: Client, user: User, logger: Logger):
    Events(client, user, logger)
    return
