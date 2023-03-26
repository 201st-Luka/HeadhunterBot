from interactions import Extension, Client, extension_command, CommandContext, Option, OptionType, Choice, extension_component, ComponentContext

from Bot.Extensions.Clan.SubcommandGroups.Components import warlog_previous_page, warlog_next_page
from Bot.Extensions.Clan.SubcommandGroups.Currentwar_Subcommands import war_stats, lineup
from Bot.Extensions.Clan.Subcommands import stats, table, warlog, clan_badge
from Bot.Extensions.Utils.autocompletes import clan_tag_auto_complete
from Database.User import User


class ClanCommand(Extension):
    client: Client
    user: User

    def __init__(self, client: Client, user: User):
        self.client = client
        self.user = user
        return

    @extension_command(
        name="clan",
        default_scope=True
    )
    async def clan(self, ctx: CommandContext, **kwargs):
        pass

    @clan.subcommand(
        name="stats",
        description="returns statistics of the clan",
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
    async def stats(self, ctx: CommandContext, **kwargs):
        await stats(ctx, kwargs)
        return

    @clan.subcommand(
        name="clan_badge",
        description="sends the clan badge",
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
    )
    async def clan_badge(self, ctx: CommandContext, **kwargs):
        await clan_badge(ctx, kwargs)
        return

    @clan.subcommand(
        name="table",
        description="returns clan member information",
        options=[
            Option(
                name="clan_tag",
                description="linked clans and clan war opponent or search clan by name or tag (type '#')",
                type=OptionType.STRING,
                required=True,
                autocomplete=True
            ),
            Option(
                name="sort",
                description="sort the table by a selected criteria",
                type=OptionType.INTEGER,
                required=False,
                choices=[
                    Choice(name="clan rank", value=0),
                    Choice(name="name", value=1),
                    Choice(name="trophies", value=2),
                    Choice(name="war", value=3),
                    Choice(name="stars", value=4),
                    Choice(name="donations", value=5),
                    Choice(name="received", value=6),
                    Choice(name="th", value=7),
                    Choice(name="role", value=8),
                    Choice(name="level", value=9),
                    Choice(name="tag", value=10)
                ]
            ),
            Option(
                name="descending",
                description="changes the order to ascending/descending",
                type=OptionType.BOOLEAN,
                required=False,
                choices=[
                    Choice(name="ascending", value=False),
                    Choice(name="descending", value=True)
                ]
            )
        ]
    )
    async def table(self, ctx: CommandContext, **kwargs):
        await table(ctx, **kwargs)
        return

    @clan.subcommand(
        name="warlog",
        description="returns the warlog of your linked clan or of the clan you have entered",
        options=[
            Option(
                name="clan_tag",
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
    )
    async def warlog(self, ctx: CommandContext, **kwargs):
        await warlog(ctx, kwargs)
        return

    @clan.group(
        name="currentwar"
    )
    async def currentwar(self, ctx: CommandContext):
        pass

    @currentwar.subcommand(
        name="war_stats",
        description="returns statistics of clans and opponent if in war",
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
    async def currentwar_war_stats(self, ctx: CommandContext, **kwargs):
        await war_stats(ctx, kwargs)
        return

    @currentwar.subcommand(
        name="lineup",
        description="returns statistics of clans and opponent if in war",
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
    async def currentwar_lineup(self, ctx: CommandContext, **kwargs):
        await lineup(ctx, kwargs)
        return

    @clan.autocomplete("clan_tag")
    async def clan_tag_autocomplete(self, ctx: CommandContext, input_str: str = None):
        await clan_tag_auto_complete(ctx, self.user, input_str)
        return

    @extension_component("button_warlog_command_next_page")
    async def button_warlog_command_next_page(self, ctx: ComponentContext):
        await warlog_next_page(ctx)
        return

    @extension_component("button_warlog_command_previous_page")
    async def button_warlog_command_previous_page(self, ctx: ComponentContext):
        await warlog_previous_page(ctx)
        return


def setup(client: Client, user: User):
    ClanCommand(client, user)
    return
