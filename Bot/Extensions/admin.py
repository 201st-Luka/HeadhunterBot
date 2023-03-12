from interactions import extension_command, Option, OptionType, Extension, Client, CommandContext, Permissions, Choice, extension_autocomplete

from Bot.Extensions.Extensionssetup import extension_command_wrapper
from CocApi.Clans.Clan import members
from CocApi.Players.Player import player
from Database.Data_base import DataBase
from Database.User import User


class AdminCommand(Extension):
    client: Client
    user: User = User(DataBase())

    def __init__(self, client: Client):
        self.client = client
        return

    @extension_command(
        name="guild_admin",
        description="server admin command",
        default_scope=True,
        options=[
            Option(
                name="user",
                description="user stuff for guild admins",
                type=OptionType.SUB_COMMAND_GROUP,
                options=[
                    Option(
                        name="force_link_player",
                        description="force links a player account to a Discord account",
                        type=OptionType.SUB_COMMAND,
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
                    ),
                    Option(
                        name="force_unlink_player",
                        description="force unlinks a player account from a Discord account",
                        type=OptionType.SUB_COMMAND,
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
                    ),
                    Option(
                        name="show_players_accounts",
                        description="shows linked ClashOfClans accounts of a player",
                        type=OptionType.SUB_COMMAND,
                        options=[
                            Option(
                                name="user",
                                description="guild user you want to execute the operation on",
                                type=OptionType.USER,
                                required=True
                            )
                        ]
                    )
                ]
            ),
            Option(
                name="guild",
                description="guild stuff for guild admins",
                type=OptionType.SUB_COMMAND_GROUP,
                options=[
                    Option(
                        name="link_clan",
                        description="sets the clan tag for your guild",
                        type=OptionType.SUB_COMMAND
                    ),
                    Option(
                        name="unset",
                        description="unsets the clan tag from your guild",
                        type=OptionType.SUB_COMMAND,
                    ),
                    Option(
                        name="info",
                        description="shows the linked clan tag of your guild",
                        type=OptionType.SUB_COMMAND
                    )
                ]
            ), Option(
                name="clan_members",
                description="clan member configuration",
                type=OptionType.SUB_COMMAND_GROUP,
                options=[
                    Option(
                        name="feed",
                        description="clan member feed configuration",
                        type=OptionType.SUB_COMMAND,
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
                                type=OptionType.INTEGER,
                                required=False,
                                choices=[
                                    Choice(name="on", value=1),
                                    Choice(name="off", value=0)
                                ]
                            )
                        ]
                    ),
                    Option(
                        name="blacklist",
                        description="player blacklist of players that are not welcome in the clan",
                        type=OptionType.SUB_COMMAND,
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
                ]
            )
        ],
        default_member_permissoins=Permissions.ADMINISTRATOR
    )
    @extension_command_wrapper
    async def guild_admin(self, ctx: CommandContext, **kwargs):
        await ctx.send(str(kwargs))
        return

    @extension_autocomplete("guild_admin", "player_tag")
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
    AdminCommand(client)
    print("loaded admin")
    return


