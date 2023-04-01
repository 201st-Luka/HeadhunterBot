from interactions import Extension, Client, extension_command, CommandContext


class PrivateCommands(Extension):
    client: Client

    def __init__(self, client: Client):
        self.client = client

    @extension_command(
        name="ping",
        default_scope=True,
        description="returns the latency between the server and the bot"
    )
    async def ping(self, ctx: CommandContext) -> None:
        await ctx.send(f"The latency between the bot and the server is {abs(round(self.client.latency))}.")

    @extension_command(
        name="guild_count",
        default_scope=True,
        description="returns the count of guilds the server is on"
    )
    async def guild_count(self, ctx: CommandContext) -> None:
        await ctx.send(f"The bot in on {len(self.client.guilds)} servers.")


def setup(client: Client) -> None:
    PrivateCommands(client)
