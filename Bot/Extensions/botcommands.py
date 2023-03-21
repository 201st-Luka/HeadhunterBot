from interactions import Extension, Client, extension_command, CommandContext, Embed

from Bot.Extensions.Extensionssetup import extension_command_wrapper
from Bot.Variables import discordServer


class ClearCommand(Extension):
    client: Client

    def __init__(self, client: Client):
        self.client = client
        return

    @extension_command(
        name="config",
        default_scope=True,
        description="This command opens the configuration guide."
    )
    @extension_command_wrapper
    async def config(self, ctx: CommandContext):
        config_embed = Embed()
        config_embed.title = "**__Configuration:__**"
        config_embed.description = "This is the configuration guide for optimal usage on a Discord guild. Follow the" \
                                   " steps to set up the HeadhunterBot."
        config_embed.add_field(name="__Step 1__",
                               value="You can link a clan to this guild using the `/linkclan` command. Enter your "
                                     "ClashOfClans clan to access more complex functions of the bot.")
        config_embed.add_field(name="__Step 2__",
                               value="Give the right permissions to the bot. The Bot must be capable of:"
                                     "\n-__Read Messages/View Channels__"
                                     "\n-__Send Messages__"
                                     "\n-__Manage Messages__"
                                     "\n-__Embed Links__"
                                     "\n-__Mention Everyone__"
                                     "\n-__Add Reactions__"
                                     "\n-__Use Slash Commands__")
        config_embed.add_field(name="__Step 3__",
                               value="Give a role to the bot which the bot admins of your guild have. Example: Your "
                                     "admins of the server have the role 'BotAdmin', so give this role to this Bot to "
                                     "enable all members having the 'BotAdmin' role to change the settings for the Bot "
                                     "on this guild.")
        await ctx.send(embeds=config_embed)
        return

    @extension_command(
        name="dc",
        default_scope=True,
        description="sends a link to the *201st Community* Discord server"
    )
    @extension_command_wrapper
    async def dc(self, ctx: CommandContext):
        await ctx.send(f"The official Discord server for the {self.client.me.name} is the [201st Community]({discordServer}) server.\n"
                       f"You can leave feedback, ask for features or get help setting up the Bot.\n"
                       f"{discordServer}")
        return


def setup(client: Client):
    ClearCommand(client)
    return
