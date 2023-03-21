from interactions import extension_command, Option, OptionType, Extension, Client, CommandContext, Permissions, Choice, extension_autocomplete

from Bot.Extensions.Extensionssetup import extension_command_wrapper
from CocApi.Clans.Clan import members
from CocApi.Players.Player import player
from Database.Data_base import DataBase
from Database.User import User


class SudoCommand(Extension):
    client: Client
    user: User = User(DataBase())

    def __init__(self, client: Client):
        self.client = client
        return

    @extension_command(
        name="sudo",
        description="server admin command",
        default_scope=True,
        default_member_permissoins=Permissions.ADMINISTRATOR
    )
    @extension_command_wrapper
    async def sudo(self, ctx: CommandContext, **kwargs):
        pass

    @sudo.subcommand(
        group="user",
        name="force_link_player",
        description="force links a player account to a Discord account",
        options=[
            Option(
                name="user",
                description="guild user you want to execute the operation on",
                type=OptionType.USER,
                required=True
            ),
            Option(
                name="player_tag",
                description="linked players or search player by tag",
                type=OptionType.STRING,
                required=True,
                autocomplete=True
            )
        ]
    )
    @extension_command_wrapper
    async def force_link_player(self, ctx: CommandContext, **kwargs):
        await ctx.send(str(kwargs))
        return

    @sudo.subcommand(
        group="user",
        name="force_unlink_player",
        description="force unlinks a player account from a Discord account",
        options=[
            Option(
                name="user",
                description="guild user you want to execute the operation on",
                type=OptionType.USER,
                required=True
            ),
            Option(
                name="player_tag",
                description="linked players or search player by tag",
                type=OptionType.STRING,
                required=True,
                autocomplete=True
            )
        ]
    )
    @extension_command_wrapper
    async def force_unlink_player(self, ctx: CommandContext, **kwargs):
        await ctx.send(str(kwargs))
        return

    @sudo.subcommand(
        group="user",
        name="show_players_accounts",
        description="shows linked ClashOfClans accounts of a player",
        options=[
            Option(
                name="user",
                description="guild user you want to execute the operation on",
                type=OptionType.USER,
                required=True
            )
        ]
    )
    @extension_command_wrapper
    async def show_players_accounts(self, ctx: CommandContext, **kwargs):
        await ctx.send(str(kwargs))
        return

    @sudo.subcommand(
        group="guild",
        name="link_clan",
        description="sets the clan tag for your guild"
    )
    @extension_command_wrapper
    async def link_clan(self, ctx: CommandContext, **kwargs):
        await ctx.send(str(kwargs))
        return

    @sudo.subcommand(
        group="guild",
        name="unset",
        description="unsets the clan tag from your guild"
    )
    @extension_command_wrapper
    async def unset(self, ctx: CommandContext, **kwargs):
        await ctx.send(str(kwargs))
        return

    @sudo.subcommand(
        group="guild",
        name="info",
        description="shows the linked clan tag of your guild"
    )
    @extension_command_wrapper
    async def info(self, ctx: CommandContext, **kwargs):
        await ctx.send(str(kwargs))
        return

    @sudo.subcommand(
        group="clan_members",
        name="feed",
        description="clan member feed configuration",
        options=[
            Option(
                name="channel",
                description="when a player joins, leaves the clan, ... a message is send in this channel",
                type=OptionType.CHANNEL,
                required=False
            ),
            Option(
                name="status",
                description="on or off",
                type=OptionType.BOOLEAN,
                required=False,
            )
        ]
    )
    @extension_command_wrapper
    async def feed(self, ctx: CommandContext, **kwargs):
        await ctx.send(str(kwargs))
        return

    @sudo.subcommand(
        group="clan_members",
        name="blacklist",
        description="player blacklist of players that are not welcome in the clan",
        options=[
            Option(
                name="player_tag",
                description="search player by tag",
                type=OptionType.STRING,
                required=False,
                autocomplete=True
            ),
            Option(
                name="dc_user",
                description="all ClashOfClans accounts linked to this player",
                type=OptionType.USER,
                required=False
            )
        ]
    )
    @extension_command_wrapper
    async def blacklist(self, ctx: CommandContext, **kwargs):
        await ctx.send(str(kwargs))
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
        await ctx.send(f"Deleted {message_amount} messages.", ephemeral=True)
        return

    @extension_autocomplete("sudo", "player_tag")
    async def player_tag_autocomplete(self, ctx: CommandContext, *args):
        choices = []
        if args != ():
            arg0 = args[0].strip('#') if args[0].startswith('#') else args[0]
            clan_tag = self.user.guilds.fetch_clantag(ctx.guild_id)
            clan_members = await members(clan_tag)
            for clan_member in clan_members['items']:
                if arg0 in clan_member['name'] or arg0 in clan_member['tag']:
                    choices.append(Choice(
                        name=f"{clan_member['name']} ({clan_member['tag']})",
                        value=" ".join((clan_member['name'], clan_member['tag']))
                    ))
            if len(choices) == 0:
                player_response = await player(arg0)
                if player_response != {"reason": "notFound"}:
                    choices.append(Choice(
                        name=f"{player_response['name']} ({player_response['tag']})",
                        value=" ".join((player_response['name'], player_response['tag']))
                    ))
        await ctx.populate(choices)
        return

def setup(client: Client):
    SudoCommand(client)
    return


