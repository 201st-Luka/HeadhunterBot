from interactions import Extension, Client, extension_command, Option, OptionType, CommandContext

from Bot.Extensions.Extensionssetup import extension_command_wrapper


class ClearCommand(Extension):
    client: Client

    def __init__(self, client: Client):
        self.client = client
        return

    @extension_command(
        name="clear",
        description="clears the chat",
        default_scope=True,
        options=[Option(name="message_amount",
                        description="the amount of messages to delete",
                        type=OptionType.INTEGER,
                        required=True)
                 ]
    )
    @extension_command_wrapper
    async def clear(self, ctx: CommandContext, message_amount: int):
        await ctx.channel.typing
        await ctx.channel.purge(message_amount)
        await ctx.send(f"Deleted {message_amount} messages.")
        return


def setup(client: Client):
    ClearCommand(client)
    return
