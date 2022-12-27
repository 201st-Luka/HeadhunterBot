from interactions import Extension, Client, extension_command, CommandContext

from Bot.Extensions.Extensionssetup import extension_command_wrapper


class PingCommand(Extension):
    client: Client

    def __init__(self, client: Client):
        self.client = client
        return

    @extension_command(
        name="ping",
        default_scope=True,
        # scope=guildIdList,
        description="This command returns the latency between bot and server."
    )
    @extension_command_wrapper
    async def ping(self, ctx: CommandContext):
        await ctx.send(f"The bot latency is {round(ctx.client.latency)}ms.")
        return


def setup(client: Client):
    PingCommand(client)
    return
