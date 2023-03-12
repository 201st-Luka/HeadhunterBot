from interactions import Extension, Client, extension_command, CommandContext, Option, OptionType, extension_autocomplete, Choice, Embed, \
    ActionRow, Button, ButtonStyle, extension_component, ComponentContext

from Bot.Exeptions import InvalidCommandSyntax
from Bot.Extensions.Clan.SubcommandGroups.Components import warlog_previous_page, warlog_next_page
from Bot.Extensions.Clan.SubcommandGroups.Currentwar_Subcommands import war_stats, lineup
from Bot.Extensions.Clan.SubcommandGroups.Link_Subcommands import set_clan, unset_clan, info_clan
from Bot.Extensions.Clan.Subcommands import stats, table, warlog, clan_badge
from Bot.Extensions.Extensionssetup import extension_command_wrapper, extension_component_wrapper
from Bot.Variables import wars_per_page as wars_p_page
from CocApi.Clans.Clan import clan
from CocApi.Clans.Clanwar import current_war, war_log
from Database.Data_base import DataBase
from Database.User import User


class ClanCommand(Extension):
    client: Client
    user: User = User(DataBase())

    def __init__(self, client: Client):
        self.client = client
        return

    @extension_command(
        name="clan",
        description="returns something",
        default_scope=True,
        options=[
            Option(
                name="stats",
                description="returns statistics of the clan",
                type=OptionType.SUB_COMMAND,
                options=[
                    Option(
                        name="clans",
                        description="linked clans and clan war opponent or search clan by name or tag (type '#')",
                        type=OptionType.STRING,
                        required=True,
                        autocomplete=True
                    )
                ]
            ),
            Option(
                name="clan_badge",
                description="sends the clan badge",
                type=OptionType.SUB_COMMAND,
                options=[
                    Option(
                        name="clans",
                        description="linked clans and clan war opponent or search clan by name or tag (type '#')",
                        type=OptionType.STRING,
                        required=True,
                        autocomplete=True
                    ),
                    Option(
                        name="size",
                        description="size of the image",
                        type=OptionType.STRING,
                        required=False,
                        choices=[
                            Choice(name="small", value="small"),
                            Choice(name="medium", value="medium"),
                            Choice(name="large", value="large")
                        ]
                    )

                ]
            ),
            Option(
                name="table",
                description="returns clan member information",
                type=OptionType.SUB_COMMAND,
                options=[
                    Option(
                        name="clans",
                        description="linked clans and clan war opponent or search clan by name or tag (type '#')",
                        type=OptionType.STRING,
                        required=True,
                        autocomplete=True
                    ),
                    Option(
                        name="sort",
                        description="sort the table by a selected criteria",
                        type=OptionType.STRING,
                        required=False,
                        choices=[
                            Choice(name="clan rank", value="0"),
                            Choice(name="name", value="1"),
                            Choice(name="trophies", value="2"),
                            Choice(name="war", value="3"),
                            Choice(name="stars", value="4"),
                            Choice(name="donations", value="5"),
                            Choice(name="received", value="6"),
                            Choice(name="th", value="7"),
                            Choice(name="role", value="8"),
                            Choice(name="level", value="9"),
                            Choice(name="tag", value="10")
                        ]
                    ),
                    Option(
                        name="order",
                        description="changes the order to ascending/descending",
                        type=OptionType.STRING,
                        required=False,
                        choices=[
                            Choice(name="ascending", value=""),
                            Choice(name="descending", value="True")
                        ]
                    )
                ]
            ),
            Option(
                name="warlog",
                description="returns the warlog of your linked clan or of the clan you have entered",
                type=OptionType.SUB_COMMAND,
                options=[
                    Option(
                        name="clans",
                        description="linked clans and clan war opponent or search clan by name or tag (type '#')",
                        type=OptionType.STRING,
                        required=True,
                        autocomplete=True
                    ),
                    Option(
                        name="page",
                        description="the page of the output",
                        type=OptionType.INTEGER,
                        required=False
                    )
                ]
            ),
            Option(
                name="link",
                description="clan linking with this server",
                type=OptionType.SUB_COMMAND_GROUP,
                options=[
                    Option(
                        name="set",
                        description="sets the clan tag for your guild",
                        type=OptionType.SUB_COMMAND,
                        options=[
                            Option(
                                name="tag",
                                description="enter your clan tag you want to set",
                                required=True,
                                type=OptionType.STRING
                            )
                        ]
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
            ),
            Option(
                name="currentwar",
                description="returns information about the current war of the clan",
                type=OptionType.SUB_COMMAND_GROUP,
                options=[
                    Option(
                        name="war_stats",
                        description="returns statistics of clans and opponent if in war",
                        type=OptionType.SUB_COMMAND,
                        options=[
                            Option(
                                name="clans",
                                description="linked clans and clan war opponent or search clan by name or tag (type '#')",
                                type=OptionType.STRING,
                                required=True,
                                autocomplete=True
                            )
                        ]
                    ),
                    Option(
                        name="lineup",
                        description="returns statistics of clans and opponent if in war",
                        type=OptionType.SUB_COMMAND,
                        options=[
                            Option(
                                name="clans",
                                description="linked clans and clan war opponent or search clan by name or tag (type '#')",
                                type=OptionType.STRING,
                                required=True,
                                autocomplete=True
                            )
                        ]
                    )
                ]
            )
        ]
    )
    @extension_command_wrapper
    async def clan(self, ctx: CommandContext, **kwargs):
        if 'sub_command_group' in kwargs:
            match kwargs['sub_command_group']:
                case 'currentwar':  # ======== CURRENTWAR command ==============================
                    match kwargs['sub_command']:
                        case 'war_stats':  # -------- war_stats subcommand ------------------
                            await war_stats(ctx, kwargs)
                            return
                        case 'lineup':  # -------- lineup subcommand ---------------------
                            await lineup(ctx, kwargs)
                            return
                        case _:  # -------- invalid subcommand --------------------
                            raise InvalidCommandSyntax
                case "link":  # ======== LINK command ====================================
                    match kwargs['sub_command']:
                        case 'set':  # -------- set subcommand-------------------------
                            await set_clan(ctx, kwargs, self.user)
                            return
                        case 'unset':  # -------- unset subcommand ----------------------
                            await unset_clan(ctx, self.user)
                            return
                        case 'info':  # -------- info subcommand -----------------------
                            await info_clan(ctx, self.user)
                            return
                        case _:
                            raise InvalidCommandSyntax
                case _:
                    raise InvalidCommandSyntax
        else:
            match kwargs['sub_command']:
                case 'stats':  # ======== STATS command ===================================
                    await stats(ctx, kwargs)
                    return
                case 'clan_badge':  # ======== CLAN_BADGE command ==============================
                    await clan_badge(ctx, kwargs)
                    return
                case "table":  # ======== TABLE command ===================================
                    await table(ctx, kwargs)
                    return
                case "warlog":  # ======== WARLOG command ==================================
                    await warlog(ctx, kwargs)
                    return
                case _:
                    raise InvalidCommandSyntax

    @extension_autocomplete("clan", "clans")
    async def stats_clans_autocomplete(self, ctx: CommandContext, *args):
        clans = [self.user.guilds.fetch_clanname_and_tag(ctx.guild_id)]
        current_war_response = await current_war(clans[0][1])
        if current_war_response['state'] != 'notInWar':
            clans.append((current_war_response['opponent']['name'], current_war_response['opponent']['tag'].strip("#")))
        if args != ():
            clan_response = await clan(args[0])
            if clan_response != {"reason": "notFound"}:
                clans.append((clan_response['name'], clan_response['tag'].strip("#")))
        choices = [Choice(name=f"{c[0]} (#{c[1]})", value=" ".join(c)) for c in clans]
        await ctx.populate(choices)
        return

    @extension_component("button_warlog_command_next_page")
    @extension_component_wrapper
    async def button_warlog_command_next_page(self, ctx: ComponentContext):
        await warlog_next_page(ctx)
        return

    @extension_component("button_warlog_command_previous_page")
    @extension_component_wrapper
    async def button_warlog_command_previous_page(self, ctx: ComponentContext):
        await warlog_previous_page(ctx)
        return


def setup(client: Client):
    ClanCommand(client)
    return
