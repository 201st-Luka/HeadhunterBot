from interactions import Extension, Client, extension_command, CommandContext, Option, OptionType, Choice, \
    extension_component, ComponentContext

from Bot.Extensions.Clan.SubcommandGroups.components import Components
from Bot.Extensions.Clan.SubcommandGroups.currentwar_sub_commands import CurrentWarSubCommands
from Bot.Extensions.Clan.sub_commands import SubCommands
from Bot.Extensions.Utils.auto_completes import AutoCompletes
from Database.user import User


class ClanCommand(Extension):
    client: Client
    user: User

    def __init__(self, client: Client, user: User):
        self.components = Components()
        self.current_war_sub_commands = CurrentWarSubCommands()
        self.sub_commands = SubCommands()
        self.auto_completes = AutoCompletes()
        self.client = client
        self.user = user

    @extension_command(name="clan", default_scope=True)
    async def clan(self, ctx: CommandContext) -> None:
        await ctx.defer()
        return

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
    async def stats(self, ctx: CommandContext, **kwargs) -> None:
        await self.sub_commands.stats(ctx, kwargs)

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
    async def clan_badge(self, ctx: CommandContext, **kwargs) -> None:
        await self.sub_commands.clan_badge(ctx, kwargs)

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
    async def table(self, ctx: CommandContext, **kwargs) -> None:
        await self.sub_commands.table(ctx, **kwargs)

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
    async def warlog(self, ctx: CommandContext, **kwargs) -> None:
        await self.sub_commands.warlog(ctx, kwargs)

    @clan.group(
        name="currentwar"
    )
    async def currentwar(self, ctx: CommandContext) -> None:
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
    async def currentwar_war_stats(self, ctx: CommandContext, **kwargs) -> None:
        await self.current_war_sub_commands.war_stats(ctx, kwargs)

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
    async def currentwar_lineup(self, ctx: CommandContext, **kwargs) -> None:
        await self.current_war_sub_commands.lineup(ctx, kwargs)

    @clan.autocomplete("clan_tag")
    async def clan_tag_autocomplete(self, ctx: CommandContext, input_str: str = None) -> None:
        await self.auto_completes.clan_tag_auto_complete(ctx, self.user, input_str)

    @extension_component("button_warlog_command_next_page")
    async def button_warlog_command_next_page(self, ctx: ComponentContext) -> None:
        await self.components.warlog_next_page(ctx)

    @extension_component("button_warlog_command_previous_page")
    async def button_warlog_command_previous_page(self, ctx: ComponentContext) -> None:
        await self.components.warlog_previous_page(ctx)


def setup(client: Client, user: User):
    ClanCommand(client, user)
