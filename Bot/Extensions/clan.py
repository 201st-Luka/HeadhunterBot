import datetime

from interactions import Extension, Client, extension_command, CommandContext, Option, OptionType, extension_autocomplete, Choice, Embed, \
    ActionRow, Button, ButtonStyle, extension_component, ComponentContext

from Bot.Exeptions import InvalidCommandSyntax, InvalidClanTag, NoClanTagLinked
from Bot.Extensions.Extensionssetup import extension_command_wrapper, extension_component_wrapper
from Bot.Methods import kwargs2clan_and_tag
from Bot.Variables import embed_color
from Bot.Variables import wars_per_page as wars_p_page
from CocApi.Clans.Clan import clan
from CocApi.Clans.Clanwar import current_war, war_log
from CocApi.Players.PLayer import player_bulk
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
                            clan_and_tag = kwargs2clan_and_tag(kwargs)
                            current_war_response = current_war(clan_and_tag[1])
                            if current_war_response == {"reason": "notFound"}:
                                raise InvalidClanTag
                            if current_war_response['state'] != 'notInWar':
                                clans_list = (
                                    (clan(clan_and_tag[1]),
                                     [war_clan for war_clan in war_log(clan_and_tag[1])['items'] if war_clan['attacksPerMember'] == 2][:20]),
                                    (clan(current_war_response['opponent']['tag'].strip('#')),
                                     [war_clan for war_clan in war_log(current_war_response['opponent']['tag'].strip('#'))['items'] if
                                      war_clan['attacksPerMember'] == 2][:20])
                                )
                                clans_embed = Embed(
                                    title=f"{current_war_response['clan']['name']} vs. {current_war_response['opponent']['name']}",
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
                                [clans_embed.add_field(
                                    name=f"{cl[0]['name']}",
                                    value=f"**{cl[0]['clanLevel']}**\n"
                                          f"**{cl[0]['warFrequency']}**\n"
                                          f"**{cl[0]['warWinStreak']}**\n"
                                          f"**{cl[0]['warWins']}** - **{cl[0]['warLosses']}** - **{cl[0]['warTies']}**\n\n"
                                          f"**{round(cl[0]['warWins'] * 100 / (cl[0]['warWins'] + cl[0]['warLosses'] + cl[0]['warTies']), 2)}%**\n"
                                          f"**{round(sum([war['teamSize'] for war in cl[1]]) / len(cl[1]), 2)}**\n"
                                          f"**{round(sum([war['clan']['stars'] for war in cl[1]]) / sum([war['clan']['attacks'] for war in cl[1]]), 2)}**\n"
                                          f"**{round(sum([war['clan']['destructionPercentage'] for war in cl[1]]) / len(cl[1]), 2)}%**",
                                    inline=True
                                ) for cl in clans_list]
                                await ctx.send(embeds=clans_embed)
                                return
                            await ctx.send(f"The clan **{clan_and_tag[0]}** (#{clan_and_tag[1]}) is not in a clan war.")
                            return
                        case 'lineup':  # -------- lineup subcommand ---------------------
                            clan_and_tag = kwargs2clan_and_tag(kwargs)
                            current_war_response = current_war(clan_and_tag[1])
                            if current_war_response == {"reason": "notFound"}:
                                raise InvalidClanTag
                            if current_war_response['state'] != 'notInWar':
                                clans_embed = Embed(
                                    title=f"{current_war_response['clan']['name']} vs. {current_war_response['opponent']['name']}"
                                )
                                clans_embed.add_field(
                                    name="Clan name",
                                    value="Average town hall level:\n"
                                          "Average hero levels:\n"
                                          "Average war stars per member:\n",
                                    inline=True
                                )
                                clan_member_list = [member for member in current_war(clan_and_tag[1])['clan']['members']]
                                clan_member_list.sort(key=lambda member: member['mapPosition'])
                                clan_member_tag_list = [member['tag'].strip('#') for member in clan_member_list]
                                opponent_member_list = [member for member in current_war(clan_and_tag[1])['opponent']['members']]
                                opponent_member_list.sort(key=lambda member: member['mapPosition'])
                                opponent_member_tag_list = [member['tag'].strip('#') for member in opponent_member_list]
                                embed_message = await ctx.send(embeds=clans_embed)
                                clans_embed.add_field(
                                    name=current_war_response['clan']['name'],
                                    value=f"**{round(sum([member['townhallLevel'] for member in current_war_response['clan']['members']]) / current_war_response['teamSize'], 2)}**",
                                    inline=True
                                )
                                message = await ctx.channel.send("This may take a moment.\nContent is loading...")
                                await ctx.channel.typing
                                clan_member_list = player_bulk(clan_member_tag_list)
                                clan_max_name_len = len(max([member['name'] for member in clan_member_list], key=len))
                                opponent_member_list = player_bulk(opponent_member_tag_list)
                                opponent_max_name_len = len(max([member['name'] for member in opponent_member_list], key=len))
                                print(clan_member_list)
                                await embed_message.edit(embeds=clans_embed)
                                await message.edit("\n".join(
                                    [
                                        f"` #  name{(clan_max_name_len - 4) * ' '}  th   K   Q   W   C | name{(opponent_max_name_len - 4) * ' '}  th   K   Q   W   C`",
                                        *[
                                            f"`{' ' + str(index + 1) if len(str(index + 1)) < 2 else index + 1}  "
                                            f"{clan_member_list[index]['name'] + (clan_max_name_len - len(str(clan_member_list[index]['name']))) * ' '}  "
                                            f"{str(clan_member_list[index]['townHallLevel']) if len(str(clan_member_list[index]['townHallLevel'])) > 1 else ' ' + str(clan_member_list[index]['townHallLevel'])}  "
                                            f"{str(clan_member_list[index]['heroes'][0]['level']) if len(clan_member_list[index]['heroes']) and len(str(clan_member_list[index]['heroes'][0]['level'])) == 2 and clan_member_list[index]['heroes'][0]['name'] == 'Barbarian King' else ' ' + str(clan_member_list[index]['heroes'][0]['level']) if len(clan_member_list[index]['heroes']) and len(clan_member_list[index]['heroes'][0]) == 1 and clan_member_list[index]['heroes'][0]['name'] == 'Barbarian King' else str(clan_member_list[index]['heroes'][1]['level']) if len(clan_member_list[index]['heroes']) > 1 and len(str(clan_member_list[index]['heroes'][1]['level'])) == 2 and clan_member_list[index]['heroes'][1]['name'] == 'Barbarian King' else ' ' + str(clan_member_list[index]['heroes'][1]['level']) if len(clan_member_list[index]['heroes']) > 1 and len(clan_member_list[index]['heroes'][1]) == 1 and clan_member_list[index]['heroes'][1]['name'] == 'Barbarian King' else '  '}  "
                                            f"{str(clan_member_list[index]['heroes'][1]['level']) if len(clan_member_list[index]['heroes']) > 1 and len(str(clan_member_list[index]['heroes'][1]['level'])) == 2 and clan_member_list[index]['heroes'][1]['name'] == 'Archer Queen' else ' ' + str(clan_member_list[index]['heroes'][1]['level']) if len(clan_member_list[index]['heroes']) > 1 and len(clan_member_list[index]['heroes'][1]) == 1 and clan_member_list[index]['heroes'][1]['name'] == 'Archer Queen' else str(clan_member_list[index]['heroes'][2]['level']) if len(clan_member_list[index]['heroes']) > 2 and len(str(clan_member_list[index]['heroes'][2]['level'])) == 2 and clan_member_list[index]['heroes'][2]['name'] == 'Archer Queen' else ' ' + str(clan_member_list[index]['heroes'][2]['level']) if len(clan_member_list[index]['heroes']) > 2 and len(clan_member_list[index]['heroes'][2]) == 1 and clan_member_list[index]['heroes'][2]['name'] == 'Archer Queen' else '  '}  "
                                            f"{str(clan_member_list[index]['heroes'][2]['level']) if len(clan_member_list[index]['heroes']) > 2 and len(str(clan_member_list[index]['heroes'][2]['level'])) == 2 and clan_member_list[index]['heroes'][2]['name'] == 'Grand Warden' else ' ' + str(clan_member_list[index]['heroes'][2]['level']) if len(clan_member_list[index]['heroes']) > 2 and len(clan_member_list[index]['heroes'][2]) == 1 and clan_member_list[index]['heroes'][2]['name'] == 'Grand Warden' else str(clan_member_list[index]['heroes'][3]['level']) if len(clan_member_list[index]['heroes']) > 3 and len(str(clan_member_list[index]['heroes'][3]['level'])) == 2 and clan_member_list[index]['heroes'][3]['name'] == 'Grand Warden' else ' ' + str(clan_member_list[index]['heroes'][3]['level']) if len(clan_member_list[index]['heroes']) > 3 and len(clan_member_list[index]['heroes'][3]) == 1 and clan_member_list[index]['heroes'][3]['name'] == 'Grand Warden' else '  '}  "
                                            f"{str(clan_member_list[index]['heroes'][3]['level']) if len(clan_member_list[index]['heroes']) > 3 and len(str(clan_member_list[index]['heroes'][3]['level'])) == 2 and clan_member_list[index]['heroes'][3]['name'] == 'Royal Champion' else ' ' + str(clan_member_list[index]['heroes'][3]['level']) if len(clan_member_list[index]['heroes']) > 3 and len(clan_member_list[index]['heroes'][3]) == 1 and clan_member_list[index]['heroes'][3]['name'] == 'Royal Champion' else str(clan_member_list[index]['heroes'][4]['level']) if len(clan_member_list[index]['heroes']) > 4 and len(str(clan_member_list[index]['heroes'][4]['level'])) == 2 and clan_member_list[index]['heroes'][4]['name'] == 'Royal Champion' else ' ' + str(clan_member_list[index]['heroes'][4]['level']) if len(clan_member_list[index]['heroes']) > 4 and len(clan_member_list[index]['heroes'][4]) == 1 and clan_member_list[index]['heroes'][4]['name'] == 'Royal Champion' else '  '}   "
                                            f"`"
                                            for index in range(current_war_response['teamSize'])
                                        ]]
                                ))
                                await ctx.channel.typing
                                return
                            await ctx.send(f"The clan **{clan_and_tag[0]}** (#{clan_and_tag[1]}) is not in a clan war.")
                            return
                        case _:  # -------- invalid subcommand --------------------
                            raise InvalidCommandSyntax
                case "link":  # ======== LINK command ====================================
                    match kwargs['sub_command']:
                        case 'set':  # -------- set subcommand-------------------------
                            if kwargs['tag'].startswith("#"):
                                kwargs['tag'] = kwargs['tag'].strip("#")
                            clan_response = clan(kwargs['tag'])
                            if clan_response == {"reason": "notFound"}:
                                await ctx.send(f"#{kwargs['tag']} is not a valid clantag!")
                                return
                            elif not self.user.guilds.fetch_clantag(ctx.guild_id) == kwargs['tag']:
                                self.user.guilds.update_clan_tag_and_name(ctx.guild_id, kwargs['tag'], clan_response['name'])
                                clan_embed = Embed(
                                    title=f"Linked {kwargs['tag']}",
                                    description=f"Successfully linked **{clan_response['name']}** #{kwargs['tag']} to this server."
                                )
                                clan_embed.set_thumbnail(url=clan_response['badgeUrls']['large'])
                                await ctx.send(embeds=clan_embed)
                                return
                            else:
                                await ctx.send(f"The clan #{kwargs['tag']} has already been linked to this server.")
                                return
                        case 'unset':  # -------- unset subcommand ----------------------
                            clan_and_tag = self.user.guilds.fetch_clanname_and_tag(ctx.guild_id)
                            if clan_and_tag != (None, None):
                                self.user.guilds.update_clan_tag_and_name(ctx.guild_id, None, None)
                                player_embed = Embed(
                                    title=f"Deleted {clan_and_tag[0]} (#{clan_and_tag[1]})",
                                    description=f"Successfully unset **{clan_and_tag[0]}** (#{clan_and_tag[1]}) from this guild."
                                )
                                await ctx.send(embeds=player_embed)
                                return
                            raise NoClanTagLinked
                        case 'info':  # -------- info subcommand -----------------------
                            clan_and_tag = self.user.guilds.fetch_clanname_and_tag(ctx.guild_id)
                            if clan_and_tag != (None, None):
                                clan_embed = Embed(
                                    title=f"Linked clan for {ctx.guild.name}",
                                    description=f"You have **{clan_and_tag[0]}** (#{clan_and_tag[1]}) linked."
                                )
                                await ctx.send(embeds=clan_embed)
                                return
                            raise NoClanTagLinked
                        case _:
                            raise InvalidCommandSyntax
                case _:
                    raise InvalidCommandSyntax
        else:
            match kwargs['sub_command']:
                case 'stats':  # ======== STATS command ===================================
                    if ' ' in kwargs['clans']:
                        clan_and_tag = kwargs2clan_and_tag(kwargs)
                        clan_and_tag[1] = kwargs['clans'].split(' ')[-1]
                        clan_response = clan(clan_and_tag[1])
                        warlog_response = [war_clan for war_clan in war_log(clan_and_tag[1])['items'] if war_clan['attacksPerMember'] == 2]
                        warlog_len = len(warlog_response)
                        if len(warlog_response) >= 20:
                            warlog_len_20 = 20
                            warlog_response_20 = warlog_response[:20]
                        else:
                            warlog_len_20 = len(warlog_response)
                            warlog_response_20 = warlog_response
                        embed_clan_info = Embed(
                            title=f"Member list for clan {clan_response['name']} ({clan_response['tag']})",
                            description=f"*{clan_response['description']}*\n"
                                        f"\nClan level: **{clan_response['clanLevel']}**\n"
                                        f"Clan points: **{clan_response['clanPoints']}**\n"
                                        f"Required trophies to join: **{clan_response['requiredTrophies']}**\n"
                                        f"Language: {clan_response['chatLanguage']['name']} ({clan_response['chatLanguage']['languageCode']})",
                            color=embed_color,
                            timestamp=datetime.datetime.now()
                        )
                        embed_clan_info.set_thumbnail(url=clan_response['badgeUrls']['large'])
                        embed_clan_info.set_footer(f"{clan_response['members']}/50 members")
                        embed_clan_info.add_field(
                            name="War",
                            value=f"War frequency: **{clan_response['warFrequency']}**\n"
                                  f"Current war win streak: **{clan_response['warWinStreak']}**\n"
                                  f"War wins - losses - ties: **{clan_response['warWins']} - {clan_response['warLosses']} - "
                                  f"{clan_response['warTies']}**\n"
                                  f"Win probability: **{round(clan_response['warWins'] * 100 / (clan_response['warWins'] + clan_response['warLosses'] + clan_response['warTies']), 2)}%**\n"
                                  f"Average team size: **{round(sum([war['teamSize'] for war in warlog_response]) / warlog_len, 2)}**\n"
                                  f"Average stars per attack: **{round(sum([war['clan']['stars'] for war in warlog_response]) / sum([war['clan']['attacks'] for war in warlog_response]), 2)}**\n"
                                  f"Average destruction percentage: **{round(sum([war['clan']['destructionPercentage'] for war in warlog_response]) / warlog_len, 2)}%**",
                            inline=True)
                        embed_clan_info.add_field(
                            name="Last 20 wars",
                            value=f"Win probability: **{sum([100 if war['result'] == 'win' else 0 for war in warlog_response_20]) / warlog_len_20}%**\n"
                                  f"Average team size: **{round(sum([war['teamSize'] for war in warlog_response_20]) / warlog_len_20, 2)}**\n"
                                  f"Average stars per attack: **{round(sum([war['clan']['stars'] for war in warlog_response_20]) / sum([war['clan']['attacks'] for war in warlog_response_20]), 2)}**\n"
                                  f"Average destruction percentage: **{round(sum([war['clan']['destructionPercentage'] for war in warlog_response_20]) / warlog_len_20, 2)}%**",
                            inline=True)
                        embed_clan_info.add_field(
                            name="\u200b",
                            value="\u200b"
                        )
                        embed_clan_info.add_field(
                            name=f"Members ({clan_response['members']}/50)",
                            value=f"Average exp level: **{round(sum([member['expLevel'] for member in clan_response['memberList']]) / clan_response['members'])}**\n"
                                  f"Average trophies: **{round(sum([member['trophies'] for member in clan_response['memberList']]) / clan_response['members'])}**\n"
                                  f"Average versus trophies: **{round(sum([member['versusTrophies'] for member in clan_response['memberList']]) / clan_response['members'])}**\n"
                                  f"Average donations: **{round(sum([member['donations'] for member in clan_response['memberList']]) / clan_response['members'])}**\n"
                                  f"Average donations received: **{round(sum([member['donationsReceived'] for member in clan_response['memberList']]) / clan_response['members'])}**",
                            inline=True)
                        embed_clan_info.add_field(
                            name=f"Clan war league",
                            value=f"Clan war league: **{clan_response['warLeague']['name']}**",
                            inline=True)
                        if clan_response['clanCapital'] != {}:
                            embed_clan_info.add_field(
                                name="Clan capital",
                                value='\n'.join([
                                    f"{district['name']} hall level: **{district['districtHallLevel']}**"
                                    for district in clan_response['clanCapital']['districts']]),
                                inline=False)
                        await ctx.send(
                            embeds=embed_clan_info,
                            components=[ActionRow(components=[
                                Button(
                                    style=ButtonStyle.LINK,
                                    label="Warlog on Cocp.it",
                                    url=f"https://cocp.it/clan/{clan_and_tag[1]}"
                                ), Button(
                                    style=ButtonStyle.LINK,
                                    label=f"{clan_response['name']} on ClashOfStats",
                                    url=f"https://www.clashofstats.com/clans/{clan_and_tag[1]}/summary"
                                )])
                            ]
                        )
                        return
                    raise InvalidClanTag
                case 'clan_badge':  # ======== CLAN_BADGE command ==============================
                    clan_and_tag = kwargs2clan_and_tag(kwargs)
                    if 'size' in kwargs:
                        size = kwargs['size']
                    else:
                        size = "medium"
                    clan_response = clan(clan_and_tag[1])
                    badge_embed = Embed(title=f"Badge of **{clan_response['name']}** #{clan_and_tag[1]}")
                    badge_embed.set_image(url=clan_response['badgeUrls'][size])
                    await ctx.send(
                        embeds=badge_embed,
                        components=[Button(
                            style=ButtonStyle.LINK,
                            label="Show in web",
                            url=clan_response['badgeUrls'][size]
                        )])
                    return
                case "table":  # ======== TABLE command ===================================
                    clan_and_tag = kwargs2clan_and_tag(kwargs)
                    clan_and_tag[1] = kwargs['clans'].split(' ')[-1]
                    response_clan = clan(clan_and_tag[1])
                    war_info = [str(response_clan['warWins']) if "warWins" in response_clan else "N/A",
                                str(response_clan['warTies']) if "warTies" in response_clan else "N/A",
                                str(response_clan['warLosses']) if "warLosses" in response_clan else "N/A"]
                    embed_clan_info = Embed(
                        title=f"Member list for clan {response_clan['name']} ({response_clan['tag']})",
                        description=f"""
                            *{response_clan['description']}*
                            \nClan level: **{response_clan['clanLevel']}**
                            Clan points: **{response_clan['clanPoints']}**
                            Required trophies to join: **{response_clan['requiredTrophies']}**
                            War frequency: **{response_clan['warFrequency']}**
                            Current war win streak: **{response_clan['warWinStreak']}**
                            War wins - losses - ties: **{war_info[0]} - {war_info[2]} - {war_info[1]}**
                            Clan war league: **{response_clan['warLeague']['name']}**
                        """,
                        color=0xFF00FF,
                        timestamp=datetime.datetime.now()
                    )
                    embed_clan_info.set_thumbnail(url=response_clan['badgeUrls']['large'])
                    embed_clan_info.set_footer(f"{response_clan['members']}/50 members")
                    await ctx.send(
                        embeds=embed_clan_info,
                        components=[ActionRow(components=[
                            Button(
                                style=ButtonStyle.LINK,
                                label="Warlog on Cocp.it",
                                url=f"https://cocp.it/clan/{clan_and_tag[1]}"
                            ), Button(
                                style=ButtonStyle.LINK,
                                label=f"{response_clan['name']} on ClashOfStats",
                                url=f"https://www.clashofstats.com/clans/{clan_and_tag[1]}/summary"
                            )])
                        ]
                    )
                    first_message = await ctx.channel.send(content="This may take a moment.\nContent is loading...")
                    await ctx.channel.typing
                    members_table_list = [
                        [
                            [position for position in response_clan['memberList'] if position['tag'] == member['tag']][0]['clanRank'],
                            member['name'],
                            member['trophies'],
                            member['warPreference'],
                            member['warStars'],
                            member['donations'],
                            member['donationsReceived'],
                            member['townHallLevel'],
                            member['role'],
                            member['expLevel'],
                            member['tag']
                        ] for member in player_bulk([member["tag"][1:] for member in response_clan["memberList"]])
                    ]
                    sort = "0" if 'sort' not in kwargs else kwargs['sort']
                    order = "" if 'order' not in kwargs else kwargs['order']
                    members_table_list.sort(key=lambda m: m[int(sort)], reverse=bool(order))
                    max_name_len, max_tag_len = len(max([name[1] for name in members_table_list], key=len)), \
                        len(max([tag[10] for tag in members_table_list], key=len))
                    members_table_list = [
                        [
                            str(member[0]) + (5 - len(str(member[0]))) * ' ' if x == 0 and len(str(member[0])) <= 5 else
                            member[1] + (max_name_len - len(member[1]) + 2) * ' ' if x == 1 and len(member[1]) <= max_name_len else
                            str(member[2]) + (10 - len(str(member[2]))) * ' ' if x == 2 and len(str(member[2])) <= 10 else
                            member[3] + (5 - len(member[3])) * ' ' if x == 3 and len(member[3]) <= 5 else
                            str(member[4]) + (7 - len(str(member[4]))) * ' ' if x == 4 and len(str(member[4])) <= 7 else
                            str(member[5]) + (11 - len(str(member[5]))) * ' ' if x == 5 and len(str(member[5])) <= 11 else
                            str(member[6]) + (10 - len(str(member[6]))) * ' ' if x == 6 and len(str(member[6])) <= 10 else
                            str(member[7]) + (4 - len(str(member[7]))) * ' ' if x == 7 and len(str(member[7])) <= 4 else
                            "leader     " if x == 8 and member[8] == "leader" else
                            "co-leader  " if x == 8 and member[8] == "coLeader" else
                            "elder      " if x == 8 and member[8] == "admin" else
                            "member     " if x == 8 and member[8] == "member" else
                            str(member[9]) + (7 - len(str(member[9]))) * ' ' if x == 9 and len(str(member[9])) <= 7 else
                            member[10] + (max_tag_len - len(member[10])) * ' ' if x == 10 and len(
                                member[10]) <= max_tag_len else None
                            for x in range(len(member))
                        ] for member in members_table_list
                    ]
                    members_table_str = [
                        [item for sublist in x for item in sublist] for x in [
                            [
                                ["`"] if i == 0 else
                                members_table_list[x] if i == 1 else
                                ["`"] if i == 2 else
                                ["\n"]
                                for i in range(4)
                            ] for x in range(len(members_table_list))
                        ]
                    ]
                    case = (len(members_table_str) - 1) // 10
                    await first_message.edit("".join((
                        "`#    name", (max_name_len - 2) * ' ', "trophies  war  stars  donations  received  th  role       level  tag",
                        (max_tag_len - 3) * ' ', "`\n",
                        *(item for outer_list in members_table_str[0:10] for item in outer_list))))
                    if case:
                        for i in range(1, case + 1):
                            await ctx.channel.send("".join(item for outer_list in members_table_str[i * 10:(i + 1) * 10] for item in outer_list))
                    return
                case "warlog":  # ======== WARLOG command ==================================
                    clan_and_tag = kwargs2clan_and_tag(kwargs)
                    page = kwargs['page'] if 'page' in kwargs else 1
                    clan_response = clan(clan_and_tag[1])
                    warlog_response = [war_clan for war_clan in war_log(clan_and_tag[1])['items'] if war_clan['attacksPerMember'] == 2]
                    max_pages = [(len(warlog_response) // wars_p_page) + 1 if len(warlog_response) % wars_p_page else len(warlog_response) // wars_p_page][0]
                    page = [1 if page <= 0 else max_pages if page > max_pages else page][0]
                    start, end = (page - 1) * wars_p_page, page * wars_p_page
                    clan_embed = Embed(
                        title=f"Warlog of {clan_response['name']} #{clan_and_tag[1]}",
                        description=f"war frequency: **{clan_response['warFrequency']}**\n"
                                    f"war win streak: **{clan_response['warWinStreak']}**\n"
                                    f"wins - losses- ties: **{clan_response['warWins']}** - **{clan_response['warLosses']}** - **{clan_response['warTies']}**\n"
                                    f"war league: **{clan_response['warLeague']['name']}**"
                    )
                    clan_embed.set_thumbnail(clan_response['badgeUrls']['large'])
                    clan_embed.set_footer(f"Page {page} of {max_pages}")
                    page_wars = warlog_response[start:end]
                    [clan_embed.add_field(
                        name=f"__{clan_war['clan']['name']} {clan_war['clan']['clanLevel']} vs {clan_war['opponent']['name']} {clan_war['opponent']['clanLevel']}__",
                        value=f"Result: **{clan_war['result']}**\n"
                              f"End date and time: **{clan_war['endTime'][6:8]}"
                              f"{['st' if clan_war['endTime'][7] == '1' else 'nd' if clan_war['endTime'][7] == '2' else 'rd' if clan_war['endTime'][7] == '3' else 'th'][0]} "
                              f"{['January' if clan_war['endTime'][4:6] == '01' else 'February' if clan_war['endTime'][4:6] == '02' else 'March' if clan_war['endTime'][4:6] == '03' else 'April' if clan_war['endTime'][4:6] == '04' else 'May' if clan_war['endTime'][4:6] == '05' else 'June' if clan_war['endTime'][4:6] == '06' else 'July' if clan_war['endTime'][4:6] == '07' else 'August' if clan_war['endTime'][4:6] == '08' else 'September' if clan_war['endTime'][4:6] == '09' else 'October' if clan_war['endTime'][4:6] == '10' else 'November' if clan_war['endTime'][4:6] == '11' else 'December'][0]} {clan_war['endTime'][0:4]}"
                              f"** at {clan_war['endTime'][9:11]}:{clan_war['endTime'][11:13]}\n"
                              f"Team size: **{clan_war['teamSize']}**\n"
                              f"Attacks: **{clan_war['clan']['attacks']}** of {clan_war['teamSize'] * 2}\n"
                              f"Stars: **{clan_war['clan']['stars']}** - **{clan_war['opponent']['stars']}**\n"
                              f"Destruction percentage: **{str(clan_war['clan']['destructionPercentage'])[:5]}** - **{str(clan_war['opponent']['destructionPercentage'])[:5]}**\n"
                              f"XP earned: **{clan_war['clan']['expEarned']}**"
                    ) for clan_war in page_wars]
                    await ctx.send(embeds=clan_embed,
                                   components=ActionRow(components=[
                                       Button(
                                           style=ButtonStyle.PRIMARY,
                                           label="Previous page",
                                           custom_id="button_warlog_command_previous_page",
                                           disabled=[True if page == 1 else False][0]
                                       ), Button(
                                           style=ButtonStyle.SECONDARY,
                                           label="Next page",
                                           custom_id="button_warlog_command_next_page",
                                           disabled=[False if page != max_pages else True][0]
                                       )
                                   ]))
                    return
                case _:
                    raise InvalidCommandSyntax

    @extension_autocomplete("clan", "clans")
    async def stats_clans_autocomplete(self, ctx: CommandContext, *args):
        clans = [self.user.guilds.fetch_clanname_and_tag(ctx.guild_id)]
        current_war_response = current_war(clans[0][1])
        if current_war_response['state'] != 'notInWar':
            clans.append((current_war_response['opponent']['name'], current_war_response['opponent']['tag'].strip("#")))
        if args != ():
            clan_response = clan(args[0])
            if clan_response != {"reason": "notFound"}:
                clans.append((clan_response['name'], clan_response['tag'].strip("#")))
        choices = [Choice(name=f"{c[0]} (#{c[1]})", value=" ".join(c)) for c in clans]
        await ctx.populate(choices)
        return

    @extension_component("button_warlog_command_next_page")
    @extension_component_wrapper
    async def button_warlog_command_next_page(self, ctx: ComponentContext):
        clan_tag = ctx.message.embeds[0].title.split(' ')[-1].strip('#')
        page = int(ctx.message.embeds[0].footer.text.split(" ")[1]) + 1
        clan_response = clan(clan_tag)
        warlog_response = [war_clan for war_clan in war_log(clan_tag)['items'] if war_clan['attacksPerMember'] == 2]
        max_pages = [(len(warlog_response) // wars_p_page) + 1 if len(warlog_response) % wars_p_page else len(warlog_response) // wars_p_page][0]
        page = [1 if page <= 0 else max_pages if page > max_pages else page][0]
        start, end = (page - 1) * wars_p_page, page * wars_p_page
        clan_embed = Embed(
            title=f"Warlog of {clan_response['name']} #{clan_tag}",
            description=f"war frequency: **{clan_response['warFrequency']}**\n"
                        f"war win streak: **{clan_response['warWinStreak']}**\n"
                        f"wins - losses- ties: **{clan_response['warWins']}** - **{clan_response['warLosses']}** - **{clan_response['warTies']}**\n"
                        f"war league: **{clan_response['warLeague']['name']}**"
        )
        clan_embed.set_thumbnail(clan_response['badgeUrls']['large'])
        clan_embed.set_footer(f"Page {page} of {max_pages}")
        page_wars = warlog_response[start:end]
        [clan_embed.add_field(
            name=f"__{clan_war['clan']['name']} {clan_war['clan']['clanLevel']} vs {clan_war['opponent']['name']} {clan_war['opponent']['clanLevel']}__",
            value=f"Result: **{clan_war['result']}**\n"
                  f"End date and time: **{clan_war['endTime'][6:8]}"
                  f"{['st' if clan_war['endTime'][7] == '1' else 'nd' if clan_war['endTime'][7] == '2' else 'rd' if clan_war['endTime'][7] == '3' else 'th'][0]} "
                  f"{['January' if clan_war['endTime'][4:6] == '01' else 'February' if clan_war['endTime'][4:6] == '02' else 'March' if clan_war['endTime'][4:6] == '03' else 'April' if clan_war['endTime'][4:6] == '04' else 'May' if clan_war['endTime'][4:6] == '05' else 'June' if clan_war['endTime'][4:6] == '06' else 'July' if clan_war['endTime'][4:6] == '07' else 'August' if clan_war['endTime'][4:6] == '08' else 'September' if clan_war['endTime'][4:6] == '09' else 'October' if clan_war['endTime'][4:6] == '10' else 'November' if clan_war['endTime'][4:6] == '11' else 'December'][0]} {clan_war['endTime'][0:4]}"
                  f"** at {clan_war['endTime'][9:11]}:{clan_war['endTime'][11:13]}\n"
                  f"Team size: **{clan_war['teamSize']}**\n"
                  f"Attacks: **{clan_war['clan']['attacks']}** of {clan_war['teamSize'] * 2}\n"
                  f"Stars: **{clan_war['clan']['stars']}** - **{clan_war['opponent']['stars']}**\n"
                  f"Destruction percentage: **{str(clan_war['clan']['destructionPercentage'])[:5]}** - **{str(clan_war['opponent']['destructionPercentage'])[:5]}**\n"
                  f"XP earned: **{clan_war['clan']['expEarned']}**"
        ) for clan_war in page_wars]
        await ctx.edit(embeds=clan_embed,
                       components=ActionRow(components=[
                           Button(
                               style=ButtonStyle.PRIMARY,
                               label="Previous page",
                               custom_id="button_warlog_command_previous_page",
                               disabled=[True if page == 1 else False][0]
                           ), Button(
                               style=ButtonStyle.SECONDARY,
                               label="Next page",
                               custom_id="button_warlog_command_next_page",
                               disabled=[False if page != max_pages else True][0]
                           )
                       ]))
        return

    @extension_component("button_warlog_command_previous_page")
    @extension_component_wrapper
    async def button_warlog_command_previous_page(self, ctx: ComponentContext):
        clan_tag = ctx.message.embeds[0].title.split(' ')[-1].strip('#')
        page = int(ctx.message.embeds[0].footer.text.split(" ")[1]) - 1
        clan_response = clan(clan_tag)
        warlog_response = [clan_war for clan_war in war_log(clan_tag)['items'] if clan_war['attacksPerMember'] == 2]
        max_pages = [(len(warlog_response) // wars_p_page) + 1 if len(warlog_response) % wars_p_page else len(warlog_response) // wars_p_page][0]
        page = [1 if page <= 0 else max_pages if page > max_pages else page][0]
        start, end = (page - 1) * wars_p_page, page * wars_p_page
        clan_embed = Embed(
            title=f"Warlog of {clan_response['name']} #{clan_tag}",
            description=f"war frequency: **{clan_response['warFrequency']}**\n"
                        f"war win streak: **{clan_response['warWinStreak']}**\n"
                        f"wins - losses- ties: **{clan_response['warWins']}** - **{clan_response['warLosses']}** - **{clan_response['warTies']}**\n"
                        f"war league: **{clan_response['warLeague']['name']}**"
        )
        clan_embed.set_thumbnail(clan_response['badgeUrls']['large'])
        clan_embed.set_footer(f"Page {page} of {max_pages}")
        page_wars = warlog_response[start:end]
        [clan_embed.add_field(
            name=f"__{clan_war['clan']['name']} {clan_war['clan']['clanLevel']} vs {clan_war['opponent']['name']} {clan_war['opponent']['clanLevel']}__",
            value=f"Result: **{clan_war['result']}**\n"
                  f"End date and time: **{clan_war['endTime'][6:8]}"
                  f"{['st' if clan_war['endTime'][7] == '1' else 'nd' if clan_war['endTime'][7] == '2' else 'rd' if clan_war['endTime'][7] == '3' else 'th'][0]} "
                  f"{['January' if clan_war['endTime'][4:6] == '01' else 'February' if clan_war['endTime'][4:6] == '02' else 'March' if clan_war['endTime'][4:6] == '03' else 'April' if clan_war['endTime'][4:6] == '04' else 'May' if clan_war['endTime'][4:6] == '05' else 'June' if clan_war['endTime'][4:6] == '06' else 'July' if clan_war['endTime'][4:6] == '07' else 'August' if clan_war['endTime'][4:6] == '08' else 'September' if clan_war['endTime'][4:6] == '09' else 'October' if clan_war['endTime'][4:6] == '10' else 'November' if clan_war['endTime'][4:6] == '11' else 'December'][0]} {clan_war['endTime'][0:4]}"
                  f"** at {clan_war['endTime'][9:11]}:{clan_war['endTime'][11:13]}\n"
                  f"Team size: **{clan_war['teamSize']}**\n"
                  f"Attacks: **{clan_war['clan']['attacks']}** of {clan_war['teamSize'] * 2}\n"
                  f"Stars: **{clan_war['clan']['stars']}** - **{clan_war['opponent']['stars']}**\n"
                  f"Destruction percentage: **{str(clan_war['clan']['destructionPercentage'])[:5]}** - **{str(clan_war['opponent']['destructionPercentage'])[:5]}**\n"
                  f"XP earned: **{clan_war['clan']['expEarned']}**"
        ) for clan_war in page_wars]
        await ctx.edit(embeds=clan_embed,
                       components=ActionRow(components=[
                           Button(
                               style=ButtonStyle.PRIMARY,
                               label="Previous page",
                               custom_id="button_warlog_command_previous_page",
                               disabled=[True if page == 1 else False][0]
                           ), Button(
                               style=ButtonStyle.SECONDARY,
                               label="Next page",
                               custom_id="button_warlog_command_next_page",
                               disabled=[False if page != max_pages else True][0]
                           )
                       ]))
        return


def setup(client: Client):
    ClanCommand(client)
    return
