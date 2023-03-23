import datetime

from interactions import CommandContext, Embed, ActionRow, Button, ButtonStyle

from Bot.Exeptions import InvalidClanTag
from Bot.Extensions.Clan.SubcommandGroups.Components import publish_warlog_embed
from Bot.Methods import clans2clan_and_tag
from Bot.Variables import embed_color
from CocApi.Clans.Clan import clan
from CocApi.Clans.Clanwar import war_log
from CocApi.Players.Player import player_bulk


async def stats(ctx: CommandContext, kwargs):
    if ' ' in kwargs['clans']:
        clan_and_tag = clans2clan_and_tag(kwargs)
        clan_and_tag[1] = kwargs['clans'].split(' ')[-1]
        clan_response = await clan(clan_and_tag[1])
        warlog_json = await war_log(clan_and_tag[1])
        warlog_response = [war_clan for war_clan in warlog_json['items'] if war_clan['attacksPerMember'] == 2]
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

async def clan_badge(ctx: CommandContext, kwargs):
    clan_and_tag = clans2clan_and_tag(kwargs)
    if 'size' in kwargs:
        size = kwargs['size']
    else:
        size = "medium"
    clan_response = await clan(clan_and_tag[1])
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

async def table(ctx: CommandContext, clans: str, sort: int = 0, order: bool = False):
    print(clans, sort, order)
    clan_and_tag = clans2clan_and_tag(clans)
    # clan_and_tag[1] = kwargs['clans'].split(' ')[-1]
    clan_and_tag[1] = clans.split(' ')[-1]
    response_clan = await clan(clan_and_tag[1])
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
            [position['clanRank'] for position in response_clan['memberList'] if position['tag'] == member['tag']][0],
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
        ] for member in await player_bulk([member["tag"][1:] for member in response_clan["memberList"]])
    ]
    # sort = 0 if 'sort' not in kwargs else kwargs['sort']
    # order = False if 'order' not in kwargs else kwargs['order']
    members_table_list.sort(key=lambda m: m[sort], reverse=order)
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

async def warlog(ctx: CommandContext, kwargs):
    clan_and_tag = clans2clan_and_tag(kwargs)
    page = kwargs['page'] if 'page' in kwargs else 1
    await publish_warlog_embed(ctx, clan_and_tag[1], page, False)
    return
