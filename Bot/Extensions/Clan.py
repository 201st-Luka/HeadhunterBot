from typing import Annotated

from interactions import Extension, SlashContext, SlashCommandOption, OptionType, SlashCommandChoice, \
    SlashCommand, Embed, Timestamp, ActionRow, Button, ButtonStyle, \
    Color
from interactions.ext.paginators import Paginator
from pyclasher import ClanWarLogRequest, ClanRequest, MISSING, ClanCurrentWarRequest
from pyclasher.models import ClanWarLogEntry
from pyclasher.bulk_requests import PlayerBulkRequest
from pyclasher.models.Enums import ClanWarResult, ClanRole, ClanWarState

from Bot.Exceptions import InvalidClanTag, NotInWar
from Bot.HeadhunterBot import HeadhunterClient
from Bot.Interactions.Converters import ClanTagConverter
from Bot.Interactions.SlashCommandOptions import ClanOption


class ClanCommand(Extension):
    def __init__(self, client: HeadhunterClient):
        self.client = client
        return

    clan = SlashCommand(name="clan")

    @clan.subcommand(
        sub_cmd_name="stats",
        sub_cmd_description="returns statistics of the clan",
        options=[
            ClanOption
        ]
    )
    async def stats(self, ctx: SlashContext, clan: Annotated[ClanRequest, ClanTagConverter]) -> None:
        warlog = await ClanWarLogRequest(clan.tag).request()
        if len(warlog) >= 20:
            warlog_len_20 = 20
            warlog_response_20 = list(warlog)[:20]
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
            color=Color.from_hex(self.client.cfg['embed_color'].strip('0x') if
                                 self.client.cfg['embed_color'].startswith('0x') else self.client.cfg['embed_color']),
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
                  f"Win probability: **"
                  f"{round(clan.war_wins * 100 / (clan.war_wins + clan.war_losses + clan.war_ties), 2)}%**\n"
                  f"Average team size: **"
                  f"{round(sum([war.team_size for war in warlog]) / len(warlog), 2)}**\n"
                  f"Average stars per attack: **"
                  f"{round(sum([war.clan.stars for war in warlog]) / sum([war.clan.attacks for war in warlog]), 2)}**\n"
                  f"Average destruction percentage: **"
                  f"{round(sum([war.clan.destruction_percentage for war in warlog]) / len(warlog), 2)}%**",
            inline=True)
        embed_clan_info.add_field(
            name="Last 20 wars",
            value=f"Win probability: **"
                  f"{sum([100 if war.result == ClanWarResult.WIN else 0 for war in warlog_response_20]) / warlog_len_20}%**\n"
                  f"Average team size: **"
                  f"{round(sum([war.team_size for war in warlog_response_20]) / warlog_len_20, 2)}**\n"
                  f"Average stars per attack: **"
                  f"{round(sum([war.clan.stars for war in warlog_response_20]) / sum([war.clan.attacks for war in warlog_response_20]), 2)}**\n"
                  f"Average destruction percentage: **"
                  f"{round(sum([war.clan.destruction_percentage for war in warlog_response_20]) / warlog_len_20, 2)}%**",
            inline=True)
        embed_clan_info.add_field(
            name="\u200b",
            value="\u200b"
        )
        embed_clan_info.add_field(
            name=f"Members ({clan.members}/50)",
            value=f"Average exp level: **"
                  f"{round(sum([member.exp_level for member in clan.member_list]) / clan.members)}**\n"
                  f"Average trophies: **"
                  f"{round(sum([member.trophies for member in clan.member_list]) / clan.members)}**\n"
                  f"Average builder base trophies: **"
                  f"{round(sum([member.builder_base_trophies for member in clan.member_list]) / clan.members)}**\n"
                  f"Average donations: **"
                  f"{round(sum([member.donations for member in clan.member_list]) / clan.members)}**\n"
                  f"Average donations received: **"
                  f"{round(sum([member.donations_received for member in clan.member_list]) / clan.members)}**",
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

    @stats.error
    async def on_stats_error(self, exception: Exception, ctx: SlashContext, clan: str = None) -> None:
        if isinstance(exception, InvalidClanTag):
            await ctx.send(str(InvalidClanTag(clan)), ephemeral=True)
        return

    @clan.subcommand(
        sub_cmd_name="badge",
        sub_cmd_description="sends the clan badge",
        options=[
            ClanOption,
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
    async def badge(self, ctx: SlashContext, clan: Annotated[ClanRequest, ClanTagConverter],
                    size: str = "medium") -> None:
        badge_embed = Embed(title=f"Badge of **{clan.name}**#{clan.tag}")
        url = clan.badge_urls.__getattribute__(size).url
        badge_embed.set_image(url=url)
        await ctx.send(
            embeds=badge_embed,
            components=Button(
                style=ButtonStyle.LINK,
                label="Show in web",
                url=url
            )
        )
        return

    @badge.error
    async def on_badge_error(self, exception: Exception, ctx: SlashContext, clan: str = None) -> None:
        if isinstance(exception, InvalidClanTag):
            await ctx.send(str(InvalidClanTag(clan)), ephemeral=True)
        return

    @clan.subcommand(
        sub_cmd_name="table",
        sub_cmd_description="returns clan member information",
        options=[
            ClanOption,
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
    async def table(self, ctx: SlashContext, clan: Annotated[ClanRequest, ClanTagConverter], sort: int = 0,
                    descending: bool = False) -> None:
        embed_clan_info = Embed(
            title=f"Member list for clan {clan.name} ({clan.tag})",
            description=f"""
                        *{clan.description}*
                        \nClan level: **{clan.clan_level}**
                        Clan points: **{clan.clan_points}**
                        Required trophies to join: **{clan.required_trophies}**
                        War frequency: **{clan.war_frequency.value}**
                        Current war win streak: **{clan.war_win_streak}**
                        War wins - losses - ties: **{clan.war_wins} - {clan.war_losses} - {clan.war_ties}**
                        Clan war league: **{clan.war_league.name}**
                    """,
            color=0xFF00FF,
            timestamp=Timestamp.now()
        )
        embed_clan_info.set_thumbnail(url=clan.badge_urls.large.url)
        embed_clan_info.set_footer(f"{clan.members}/50 members")
        await ctx.send(
            embeds=embed_clan_info,
            components=Button(
                style=ButtonStyle.LINK,
                label=f"{clan.name} on ClashOfStats",
                url=f"https://www.clashofstats.com/clans/{clan.tag.strip('#')}/summary"
            )
        )

        first_message = await ctx.channel.send(content="This may take a moment.\nContent is loading...")
        await ctx.channel.trigger_typing()

        player_bulk = PlayerBulkRequest.from_member_list(clan.member_list)
        await player_bulk.request()

        members_table_list = [
            [
                i + 1,
                player.name,
                player.trophies,
                player.war_preference,
                player.war_stars,
                player.donations,
                player.donations_received,
                player.town_hall_level,
                "leader" if player.role == ClanRole.LEADER else "co-leader" if player.role == ClanRole.COLEADER else
                "elder" if player.role == ClanRole.ADMIN else "member",
                player.exp_level,
                player.tag
            ] for i, player in enumerate(player_bulk)
        ]
        members_table_list.sort(key=lambda m: m[sort], reverse=descending)
        max_name_len, max_tag_len = max([len(member[1]) for member in members_table_list] + [4]), \
            max(len(member[10]) for member in members_table_list)
        members_table_str = [
            f"`{member[0]:3}  "
            f"{member[1]:{max_name_len}}  "
            f"{member[2]:8}  "
            f"{member[3].value:3}  "
            f"{member[4]:5}  "
            f"{member[5]:9}  "
            f"{member[6]:8}  "
            f"{member[7]:2}  "
            f"{member[8]:9}  "
            f"{member[9]:5}  "
            f"{member[10]:{max_tag_len}}`"
            for member in members_table_list
        ]

        await first_message.edit(content="\n".join((
            f"` #   {'name':{max_name_len}}  trophies  war  stars  donations  "
            f"received  th  role       level  {'tag':{max_tag_len}}`",
            *(item for item in members_table_str[0:10])
        )))
        if case := (len(members_table_str) - 1) // 10:
            for i in range(1, case + 1):
                await ctx.channel.send(
                    "\n".join(item for item in members_table_str[i * 10:(i + 1) * 10]))
        return

    @table.error
    async def on_table_error(self, exception: Exception, ctx: SlashContext, clan: str = None) -> None:
        if isinstance(exception, InvalidClanTag):
            await ctx.send(str(InvalidClanTag(clan)), ephemeral=True)
        return

    @clan.subcommand(
        sub_cmd_name="warlog",
        sub_cmd_description="returns the warlog of your linked clan or of the clan you have entered",
        options=[
            ClanOption,
            SlashCommandOption(
                name="page",
                description="the page of the output",
                type=OptionType.INTEGER,
                required=False
            )
        ]
    )
    async def warlog(self, ctx: SlashContext, clan: Annotated[ClanRequest, ClanTagConverter], page: int = 1) -> None:
        warlog_request = await ClanWarLogRequest(clan.tag).request()
        warlog = [war for war in warlog_request if war.attacks_per_member == 2]
        clan_embeds: list[Embed] = []

        for start in range(*slice(0, None, self.client.cfg['wars_per_page']).indices(len(warlog))):
            embed = Embed(
                title=f"Warlog of {clan.name} {clan.tag}",
                description=f"war frequency: **{clan.war_frequency.value}**\n"
                            f"war win streak: **{clan.war_win_streak}**\n"
                            f"wins - losses- ties: **{clan.war_wins}** - **{clan.war_losses}** - **{clan.war_ties}**\n"
                            f"war league: **{clan.war_league.name}**"
            )
            embed.set_thumbnail(clan.badge_urls.large.url)

            for war in warlog[start:start + self.client.cfg['wars_per_page']]:
                match war.end_time.day:
                    case 1:
                        day = f"{war.end_time.day}st"
                    case 21:
                        day = f"{war.end_time.day}st"
                    case 31:
                        day = f"{war.end_time.day}st"
                    case 2:
                        day = f"{war.end_time.day}nd"
                    case 22:
                        day = f"{war.end_time.day}nd"
                    case 3:
                        day = f"{war.end_time.day}rd"
                    case 23:
                        day = f"{war.end_time.day}rd"
                    case _:
                        day = f"{war.end_time.day}th"
                match war.end_time.month:
                    case 1:
                        month = "January"
                    case 2:
                        month = "February"
                    case 3:
                        month = "March"
                    case 4:
                        month = "April"
                    case 5:
                        month = "May"
                    case 6:
                        month = "June"
                    case 7:
                        month = "Juny"
                    case 8:
                        month = "August"
                    case 9:
                        month = "September"
                    case 10:
                        month = "October"
                    case 11:
                        month = "November"
                    case 12:
                        month = "December"
                    case _:
                        month = MISSING

                embed.add_field(
                    name=f"__{war.clan.name} ({war.clan.clan_level}) vs {war.opponent.name} "
                         f"({war.opponent.clan_level})__",
                    value=f"Result: **{war.result.value}**\n"
                          f"End date and time: **{day} {month} {war.end_time.year}"
                          f"** at {war.end_time.hour}:{war.end_time.minute}\n"
                          f"Team size: **{war.team_size}**\n"
                          f"Attacks: **{war.clan.attacks}** of {war.team_size * 2}\n"
                          f"Stars: **{war.clan.stars}** - **{war.opponent.stars}**\n"
                          f"Destruction percentage: **{war.clan.destruction_percentage:5}** - *"
                          f"*{war.opponent.destruction_percentage:5}**\n"
                          f"XP earned: **{war.clan.exp_earned}**"
                )

            clan_embeds.append(embed)

        paginator = Paginator.create_from_embeds(self.client, *clan_embeds)
        paginator.page_index = page - 1
        paginator.show_select_menu = True
        paginator.default_color = Color.from_hex(
            self.client.cfg['embed_color'].strip('0x') if
            self.client.cfg['embed_color'].startswith('0x') else
            self.client.cfg['embed_color']
        )

        await paginator.send(ctx)
        return

    @warlog.error
    async def on_warlog_error(self, exception: Exception, ctx: SlashContext, clan: str = None) -> None:
        if isinstance(exception, InvalidClanTag):
            await ctx.send(str(InvalidClanTag(clan)), ephemeral=True)
        return

    currentwar = clan.group(name="currentwar")

    @currentwar.subcommand(
        sub_cmd_name="stats",
        sub_cmd_description="returns statistics of clans and opponent if in war",
        options=[
            ClanOption
        ]
    )
    async def stats(self, ctx: SlashContext, clan: Annotated[ClanRequest, ClanTagConverter]) -> None:
        current_war = await ClanCurrentWarRequest(clan.tag).request()
        if current_war.state != ClanWarState.NOT_IN_WAR:
            clan_warlog = await ClanWarLogRequest(clan.tag).request()
            opponent_warlog = await ClanWarLogRequest(current_war.opponent.tag).request()
            clans_list: tuple[tuple[ClanRequest, list[ClanWarLogEntry]], tuple[ClanRequest, list[ClanWarLogEntry]]] = (
                (clan,
                 [war for war in clan_warlog if war.attacks_per_member == 2][:20]),
                (await ClanRequest(current_war.opponent.tag).request(),
                 [war for war in opponent_warlog if war.attacks_per_member == 2][:20])
            )
            clans_embed = Embed(
                title=f"{current_war.clan.name} vs. {current_war.opponent.name}",
                color=Color.from_hex(
                    self.client.cfg['embed_color'].strip('0x') if
                    self.client.cfg['embed_color'].startswith('0x') else
                    self.client.cfg['embed_color']
                )
            )
            clans_embed.add_field(
                name="Name:",
                value="Clan level:\n"
                      "War frequency:\n"
                      "Current war win streak:\n"
                      "War wins - losses - ties:\n"
                      "__Last 20 clan wars:__\n"
                      "Win probability:\n"
                      "Average team size:\n"
                      "Average stars per attack:\n"
                      "Average destruction percentage:\n",
                inline=True
            )
            for cl in clans_list:
                clans_embed.add_field(
                    name=f"{cl[0].name}",
                    value=f"**{cl[0].clan_level}**\n"
                          f"**{cl[0].war_frequency.value}**\n"
                          f"**{cl[0].war_win_streak}**\n"
                          f"**{cl[0].war_wins}** - **{cl[0].war_losses}** - **{cl[0].war_ties}**\n\n"
                          f"**{round(cl[0].war_wins * 100 / (cl[0].war_wins + cl[0].war_losses + cl[0].war_ties), 2)}%**\n"
                          f"**{round(sum([war.team_size for war in cl[1]]) / len(cl[1]), 2)}**\n"
                          f"**{round(sum([war.clan.stars for war in cl[1]]) / sum([war.clan.attacks for war in cl[1]]), 2)}**\n"
                          f"**{round(sum([war.clan.destruction_percentage for war in cl[1]]) / len(cl[1]), 2)}%**",
                    inline=True
                )
            await ctx.send(embeds=clans_embed)
            return

        raise NotInWar

    @stats.error
    async def on_stats_error(self, exception: Exception, ctx: SlashContext, clan: str = None) -> None:
        if isinstance(exception, InvalidClanTag):
            await ctx.send(str(InvalidClanTag(clan)), ephemeral=True)
        if isinstance(exception, NotInWar):
            await ctx.send(str(NotInWar))
        return

    @currentwar.subcommand(
        sub_cmd_name="lineup",
        sub_cmd_description="returns statistics of clans and opponent if in war",
        options=[
            ClanOption
        ]
    )
    async def lineup(self, ctx: SlashContext, clan: Annotated[ClanRequest, ClanTagConverter]) -> None:
        current_war = await ClanCurrentWarRequest(clan.tag).request()
        if current_war.state != ClanWarState.NOT_IN_WAR:
            clans_embed = Embed(
                title=f"{current_war.clan.name} vs. {current_war.opponent.name}",
                color=Color.from_hex(self.client.cfg['embed_color'].strip('0x') if
                                     self.client.cfg['embed_color'].startswith('0x') else
                                     self.client.cfg['embed_color'])
            )
            clans_embed.add_field(
                name="Clan name",
                value="Average town hall level:\n"
                      "Average war stars per member:\n",
                inline=True
            )

            clan_member_list = [member for member in current_war.clan.members]
            clan_member_list.sort(key=lambda member: member.map_position)
            opponent_member_list = [member for member in current_war.opponent.members]
            opponent_member_list.sort(key=lambda member: member.map_position)
            embed_message = await ctx.send(embeds=clans_embed)
            message = await ctx.channel.send("This may take a moment.\nContent is loading...")

            clan_players = await PlayerBulkRequest((member.tag for member in clan_member_list)).request()
            clan_max_name_len = max([len(player.name) for player in clan_players] + [4])
            opponent_players = await PlayerBulkRequest((member.tag for member in opponent_member_list)).request()
            opponent_max_name_len = max([len(player.name) for player in opponent_players] + [4])

            clans_embed.add_field(
                name=current_war.clan.name,
                value=f"**{round(sum([member.townhall_level for member in current_war.clan.members]) / current_war.team_size, 2)}**\n"
                      f"**{round(sum((cp.war_stars for cp in clan_players)) / len(clan_players), 2)}**",
                inline=True
            )
            clans_embed.add_field(
                name=current_war.opponent.name,
                value=f"**{round(sum([member.townhall_level for member in current_war.opponent.members]) / current_war.team_size, 2)}**\n"
                      f"**{round(sum((op.war_stars for op in opponent_players)) / len(opponent_players), 2)}**",
                inline=True
            )

            await embed_message.edit(embeds=clans_embed)

            content = [
                f"` #  {'name':{clan_max_name_len}}  th   K   Q   W   C | {'name':{opponent_max_name_len}}  th   K"
                f"   Q   W   C`"
            ]
            for i, (clan_player, opponent_player) in enumerate(zip(clan_players, opponent_players)):
                cp_king_level = "  "
                cp_queen_level = "  "
                cp_warden_level = "  "
                cp_champ_level = "  "
                for item in clan_player.heroes:
                    match item.name:
                        case 'Barbarian King':
                            cp_king_level = item.level
                        case 'Archer Queen':
                            cp_queen_level = item.level
                        case 'Grand Warden':
                            cp_warden_level = item.level
                        case 'Royal Champion':
                            cp_champ_level = item.level
                op_king_level = "  "
                op_queen_level = "  "
                op_warden_level = "  "
                op_champ_level = "  "
                for item in opponent_player.heroes:
                    match item.name:
                        case 'Barbarian King':
                            op_king_level = item.level
                        case 'Archer Queen':
                            op_queen_level = item.level
                        case 'Grand Warden':
                            op_warden_level = item.level
                        case 'Royal Champion':
                            op_champ_level = item.level

                content.append(
                    f"`{i + 1:2}  "
                    f"{clan_player.name:{clan_max_name_len}}  "
                    f"{clan_player.town_hall_level:2}  "
                    f"{cp_king_level:2}  {cp_queen_level:2}  {cp_warden_level:2}  {cp_champ_level:2} | "
                    f"{opponent_player.name:{opponent_max_name_len}}  "
                    f"{opponent_player.town_hall_level:2}  "
                    f"{op_king_level:2}  {op_queen_level:2}  {op_warden_level:2}  {op_champ_level:2}`"
                )

            await message.edit(content="\n".join(content[0:21]))
            if len(content) >= 21:
                await ctx.channel.send("\n".join(content[21:41]))
            if len(content) >= 41:
                await ctx.channel.send("\n".join(content[41:]))
            return

        raise NotInWar

    @lineup.error
    async def on_lineup_error(self, exception: Exception, ctx: SlashContext, clan: str = None) -> None:
        if isinstance(exception, InvalidClanTag):
            await ctx.send(str(InvalidClanTag(clan)), ephemeral=True)
        if isinstance(exception, NotInWar):
            await ctx.send(str(NotInWar))
        return


def setup(client: HeadhunterClient):
    ClanCommand(client)
