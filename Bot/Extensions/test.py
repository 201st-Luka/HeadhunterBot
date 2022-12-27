from interactions import Extension, Client, extension_command, Option, OptionType, extension_autocomplete, CommandContext, Choice

from Bot.Extensions.Extensionssetup import extension_command_wrapper


class TestCommand(Extension):
    client: Client

    def __init__(self, client: Client):
        self.client = client
        return

    @extension_command(
        name="test",
        description="just a test command",
        default_scope=True,
        options=[Option(name="test_option",
                        description="test_option_description",
                        type=OptionType.STRING,
                        required=True,
                        autocomplete=True)
                 ]
    )
    @extension_command_wrapper
    async def test(self, ctx: CommandContext, **kwargs):
        await ctx.send(str(kwargs))
        return

    @extension_autocomplete("test", "test_option")
    async def test_autocomplete(self, ctx: CommandContext, value=""):
        items = ["eins", "zwei", "drei", "vier", "fünf", "..."]
        choices = [Choice(name=item, value=item) for item in items if value in item]
        await ctx.populate(choices)
        return


def setup(client: Client):
    TestCommand(client)
    return
