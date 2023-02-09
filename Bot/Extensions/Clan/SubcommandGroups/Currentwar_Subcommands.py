from interactions import Embed, CommandContext

from Bot.Exeptions import InvalidClanTag
from Bot.Methods import kwargs2clan_and_tag
from CocApi.Clans.Clan import clan
from CocApi.Clans.Clanwar import current_war, war_log
from CocApi.Players.Player import player_bulk


async def war_stats(ctx: CommandContext, kwargs):
    clan_and_tag = kwargs2clan_and_tag(kwargs)
    current_war_response = await current_war(clan_and_tag[1])
    if current_war_response == {"reason": "notFound"}:
        raise InvalidClanTag
    if current_war_response['state'] != 'notInWar':
        warlog_json = await war_log(clan_and_tag[1])
        warlog_json_opponent = await war_log(current_war_response['opponent']['tag'].strip('#'))
        clans_list = (
            (await clan(clan_and_tag[1]),
             [war_clan for war_clan in warlog_json['items'] if war_clan['attacksPerMember'] == 2][:20]),
            (await clan(current_war_response['opponent']['tag'].strip('#')),
             [war_clan for war_clan in warlog_json_opponent['items'] if
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

async def lineup(ctx: CommandContext, kwargs):
    clan_and_tag = kwargs2clan_and_tag(kwargs)
    current_war_response = await current_war(clan_and_tag[1])
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
        clan_member_list = [member for member in current_war_response['clan']['members']]
        clan_member_list.sort(key=lambda member: member['mapPosition'])
        clan_member_tag_list = [member['tag'].strip('#') for member in clan_member_list]
        opponent_member_list = [member for member in current_war_response['opponent']['members']]
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
        clan_member_list = await player_bulk(clan_member_tag_list)
        clan_max_name_len = len(max([member['name'] for member in clan_member_list], key=len))
        opponent_member_list = await player_bulk(opponent_member_tag_list)
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

