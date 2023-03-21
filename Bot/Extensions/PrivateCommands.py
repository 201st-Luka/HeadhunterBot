from interactions import Extension, Client, extension_command, CommandContext

from Bot.Extensions.Extensionssetup import extension_command_wrapper


class PrivateCommands(Extension):
    client: Client

    def __init__(self, client: Client):
        self.client = client
        return

    @extension_command(
        name="ping",
        default_scope=True,
        description="returns the latency between the server and the bot"
    )
    @extension_command_wrapper
    async def ping(self, ctx: CommandContext):
        await ctx.send(f"The latency between the bot and the server is {abs(round(self.client.latency))}.")
        return

    @extension_command(
        name="guild_count",
        default_scope=True,
        description="returns the count of guilds the server is on"
    )
    @extension_command_wrapper
    async def guild_count(self, ctx: CommandContext):
        await ctx.send(f"The bot in on {len(self.client.guilds)} servers.")
        return

def setup(client: Client):
    PrivateCommands(client)
    return
