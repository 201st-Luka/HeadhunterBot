import datetime

from interactions import Extension, Client, extension_command, CommandContext, Option, OptionType, extension_autocomplete, Choice, Embed, \
    ActionRow, Button, ButtonStyle

from Bot.Exeptions import InvalidCommandSyntax, InvalidClanTag
from Bot.Extensions.Extensionssetup import extension_command_wrapper
from Bot.Methods import kwargs2clan_and_tag
from Bot.Variables import embed_color
from CocApi.Clans.Clan import clan
from CocApi.Clans.Clanwar import current_war, war_log
from CocApi.Players.PLayer import player, player_bulk
from Database.Data_base import DataBase
from Database.User import User


class ClanCommand(Extension):
    client: Client
    user: User = User(DataBase())

    def __init__(self, client: Client):
        self.client = client
        return

    @extension_command(name="clan",
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
                                       description="linked clans and clan war opponent",
                                       type=OptionType.STRING,
                                       required=True,
                                       autocomplete=True)
                               ]
                           ),
                           Option(
                               name="clan_badge",
                               description="sends the clan badge",
                               type=OptionType.SUB_COMMAND,
                               options=[
                                   Option(
                                       name="clans",
                                       description="linked clans and clan war opponent",
                                       type=OptionType.STRING,
                                       required=True,
                                       autocomplete=True),
                                   Option(
                                       name="size",
                                       description="size of the image",
                                       type=OptionType.STRING,
                                       required=False,
                                       choices=[Choice(name="small", value="small"),
                                                Choice(name="medium", value="medium"),
                                                Choice(name="large", value="large")
                                                ]
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
                                               description="linked clans and clan war opponent",
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
                                               description="linked clans and clan war opponent",
                                               type=OptionType.STRING,
                                               required=True,
                                               autocomplete=True
                                           )
                                       ]
                                   )
                               ]
                           )
                       ])
    @extension_command_wrapper
    async def clan(self, ctx: CommandContext, **kwargs):
        if 'sub_command_group' in kwargs:
            match kwargs['sub_command_group']:
                case 'currentwar':
                    match kwargs['sub_command']:
                        case 'war_stats':
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
                        case 'lineup':
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
                                    [f"` #  name{(clan_max_name_len - 4) * ' '}  th   K   Q   W   C | name{(opponent_max_name_len - 4) * ' '}  th   K   Q   W   C`",
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
                        case _:
                            raise InvalidCommandSyntax
                case _:
                    raise InvalidCommandSyntax
        else:
            match kwargs['sub_command']:
                case 'stats':
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
                case 'clan_badge':
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


def setup(client: Client):
    ClanCommand(client)
    return
