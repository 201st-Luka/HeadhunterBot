from interactions import Extension, SlashContext, SlashCommandOption, OptionType, SlashCommandChoice, \
    ComponentContext, component_callback, SlashCommand, AutoDefer, Embed, Timestamp, ActionRow, Button, ButtonStyle

from pyclasher import ClanWarLogRequest, ClanRequest
from pyclasher.models import ClanWarResult

# from Bot.Extensions.clan.SubcommandGroups.components import Components
# from Bot.Extensions.clan.SubcommandGroups.currentwar_sub_commands import CurrentWarSubCommands
# from Bot.Extensions.clan.sub_commands import SubCommands
# from Bot.Extensions.Utils.auto_completes import AutoCompletes
from Bot.HeadhunterBot import HeadhunterClient
from Bot.Exceptions import InvalidClanTag
from Bot.Converters.PyClasher import ClanConverter
from Database.user import User


class ClanCommand(Extension):
    def __init__(self, client: HeadhunterClient):
        self.client = client
        return

    clan = SlashCommand(name="clan", auto_defer=AutoDefer(enabled=True))

    @clan.subcommand(
        sub_cmd_name="stats",
        sub_cmd_description="returns statistics of the clan",
        options=[
            SlashCommandOption(
                name="clan",
                description="linked clans and clan war opponent or search clan by name or tag (type '#')",
                type=OptionType.STRING,
                required=True,
                autocomplete=True
            )
        ]
    )
    async def stats(self, ctx: SlashContext, clan: ClanConverter | ClanRequest, **kwargs) -> None:
        warlog = ClanWarLogRequest(clan.tag).request()
        if len(warlog) >= 20:
            warlog_len_20 = 20
            warlog_response_20 = warlog[:20]
        else:
            warlog_len_20 = len(warlog)
            warlog_response_20 = warlog
        embed_clan_info = Embed(
            title=f"Member list for clan {clan.name} ({clan.tag})",
            description=f"*{clan.description}*\n"
                        f"\nClan level: **{clan.clan_level}**\n"
                        f"Clan points: **{clan.clan_points}**\n"
                        f"Required trophies to join: **{clan.required_trophies}**\n"
                        f"Language: {clan.chat_language.name} ({clan.chat_language.language_code})",
            color=self.client.cfg['embed_color'],
            timestamp=Timestamp.now()
        )
        embed_clan_info.set_thumbnail(url=clan.badge_urls.large.url)
        embed_clan_info.set_footer(f"{clan.members}/50 members")
        embed_clan_info.add_field(
            name="War",
            value=f"War frequency: **{clan.war_frequency}**\n"
                  f"Current war win streak: **{clan.war_win_streak}**\n"
                  f"War wins - losses - ties: **{clan.war_wins} - {clan.war_losses} - "
                  f"{clan.war_ties}**\n"
                  f"Win probability: **{round(clan.war_wins * 100 / (clan.war_wins + clan.war_losses + clan.war_ties), 2)}%**\n"
                  f"Average team size: **{round(sum([war.team_size for war in warlog]) / len(warlog), 2)}**\n"
                  f"Average stars per attack: **{round(sum([war.clan.stars for war in warlog]) / sum([war.clan.attacks for war in warlog]), 2)}**\n"
                  f"Average destruction percentage: **{round(sum([war.clan.destruction_percentage for war in warlog]) / len(warlog), 2)}%**",
            inline=True)
        embed_clan_info.add_field(
            name="Last 20 wars",
            value=f"Win probability: **{sum([100 if war.result == ClanWarResult.WIN else 0 for war in warlog_response_20]) / warlog_len_20}%**\n"
                  f"Average team size: **{round(sum([war.team_size for war in warlog_response_20]) / warlog_len_20, 2)}**\n"
                  f"Average stars per attack: **{round(sum([war.clan.stars for war in warlog_response_20]) / sum([war.clan.attacks for war in warlog_response_20]), 2)}**\n"
                  f"Average destruction percentage: **{round(sum([war.clan.destruction_percentage for war in warlog_response_20]) / warlog_len_20, 2)}%**",
            inline=True)
        embed_clan_info.add_field(
            name="\u200b",
            value="\u200b"
        )
        embed_clan_info.add_field(
            name=f"Members ({clan.members}/50)",
            value=f"Average exp level: **{round(sum([member.exp_level for member in clan.member_list]) / clan.members)}**\n"
                  f"Average trophies: **{round(sum([member.trophies for member in clan.member_list]) / clan.members)}**\n"
                  f"Average versus trophies: **{round(sum([member.versus_trophies for member in clan.member_list]) / clan.members)}**\n"
                  f"Average donations: **{round(sum([member.donations for member in clan.member_list]) / clan.members)}**\n"
                  f"Average donations received: **{round(sum([member.donations_received for member in clan.member_list]) / clan.members)}**",
            inline=True
        )
        embed_clan_info.add_field(
            name=f"Clan war league",
            value=f"Clan war league: **{clan.war_league.name}**",
            inline=True
        )
        if clan.clan_capital != {}:
            embed_clan_info.add_field(
                name="Clan capital",
                value='\n'.join([
                    f"{district.name} hall level: **{district.district_hall_level}**"
                    for district in clan.clan_capital.districts]),
                inline=False
            )
        await ctx.send(
            embeds=embed_clan_info,
            components=[ActionRow(
                Button(
                    style=ButtonStyle.LINK,
                    label=f"{clan.name} on ClashOfStats",
                    url=f"https://www.clashofstats.com/clans/{clan.tag.strip('#')}/summary"
                ))
            ]
        )
        return

    @clan.subcommand(
        sub_cmd_name="clan_badge",
        sub_cmd_description="sends the clan badge",
        options=[
            SlashCommandOption(
                name="clan_tag",
                description="linked clans and clan war opponent or search clan by name or tag (type '#')",
                type=OptionType.STRING,
                required=True,
                autocomplete=True
            ),
            SlashCommandOption(
                name="size",
                description="size of the image",
                type=OptionType.STRING,
                required=False,
                choices=[
                    SlashCommandChoice(name="small", value="small"),
                    SlashCommandChoice(name="medium", value="medium"),
                    SlashCommandChoice(name="large", value="large")
                ]
            )
        ]
    )
    async def clan_badge(self, ctx: SlashContext, **kwargs) -> None:
        await self.sub_commands.clan_badge(ctx, **kwargs)

    @clan.subcommand(
        sub_cmd_name="table",
        sub_cmd_description="returns clan member information",
        options=[
            SlashCommandOption(
                name="clan_tag",
                description="linked clans and clan war opponent or search clan by name or tag (type '#')",
                type=OptionType.STRING,
                required=True,
                autocomplete=True
            ),
            SlashCommandOption(
                name="sort",
                description="sort the table by a selected criteria",
                type=OptionType.INTEGER,
                required=False,
                choices=[
                    SlashCommandChoice(name="clan rank", value=0),
                    SlashCommandChoice(name="name", value=1),
                    SlashCommandChoice(name="trophies", value=2),
                    SlashCommandChoice(name="war", value=3),
                    SlashCommandChoice(name="stars", value=4),
                    SlashCommandChoice(name="donations", value=5),
                    SlashCommandChoice(name="received", value=6),
                    SlashCommandChoice(name="th", value=7),
                    SlashCommandChoice(name="role", value=8),
                    SlashCommandChoice(name="level", value=9),
                    SlashCommandChoice(name="tag", value=10)
                ]
            ),
            SlashCommandOption(
                name="descending",
                description="changes the order to ascending/descending",
                type=OptionType.BOOLEAN,
                required=False,
                choices=[
                    SlashCommandChoice(name="ascending", value=False),
                    SlashCommandChoice(name="descending", value=True)
                ]
            )
        ]
    )
    async def table(self, ctx: SlashContext, **kwargs) -> None:
        await self.sub_commands.table(ctx, **kwargs)

    @clan.subcommand(
        sub_cmd_name="warlog",
        sub_cmd_description="returns the warlog of your linked clan or of the clan you have entered",
        options=[
            SlashCommandOption(
                name="clan_tag",
                description="linked clans and clan war opponent or search clan by name or tag (type '#')",
                type=OptionType.STRING,
                required=True,
                autocomplete=True
            ),
            SlashCommandOption(
                name="page",
                description="the page of the output",
                type=OptionType.INTEGER,
                required=False
            )
        ]
    )
    async def warlog(self, ctx: SlashContext, **kwargs) -> None:
        await self.sub_commands.warlog(ctx, **kwargs)

    currentwar = clan.group(name="currentwar")

    @currentwar.subcommand(
        sub_cmd_name="war_stats",
        sub_cmd_description="returns statistics of clans and opponent if in war",
        options=[
            SlashCommandOption(
                name="clan_tag",
                description="linked clans and clan war opponent or search clan by name or tag (type '#')",
                type=OptionType.STRING,
                required=True,
                autocomplete=True
            )
        ]
    )
    async def currentwar_war_stats(self, ctx: SlashContext, **kwargs) -> None:
        await self.current_war_sub_commands.war_stats(ctx, **kwargs)

    @currentwar.subcommand(
        sub_cmd_name="lineup",
        sub_cmd_description="returns statistics of clans and opponent if in war",
        options=[
            SlashCommandOption(
                name="clan_tag",
                description="linked clans and clan war opponent or search clan by name or tag (type '#')",
                type=OptionType.STRING,
                required=True,
                autocomplete=True
            )
        ]
    )
    async def currentwar_lineup(self, ctx: SlashContext, **kwargs) -> None:
        await self.current_war_sub_commands.lineup(ctx, **kwargs)

    @clan.autocomplete("clan_tag")
    async def clan_tag_autocomplete(self, ctx: SlashContext, input_str: str = None) -> None:
        await self.auto_completes.clan_tag_auto_complete(ctx, self.user, input_str)

    @component_callback("button_warlog_command_next_page")
    async def button_warlog_command_next_page(self, ctx: ComponentContext) -> None:
        await self.components.warlog_next_page(ctx)

    @component_callback("button_warlog_command_previous_page")
    async def button_warlog_command_previous_page(self, ctx: ComponentContext) -> None:
        await self.components.warlog_previous_page(ctx)


def setup(client: HeadhunterClient):
    ClanCommand(client)
