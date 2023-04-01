from interactions import Embed, CommandContext

from Bot.exceptions import InvalidClanTag
from Bot.methods import Methods
from API.Clans.clan import Clan
from API.Clans.clan_war import ClanWar
from API.Players.player import Player


class CurrentWarSubCommands:
    def __init__(self):
        self.methods = Methods()
        self.clan = Clan()
        self.clan_war = ClanWar()
        self.player = Player()

    async def war_stats(self, ctx: CommandContext, kwargs) -> None:
        clan_and_tag = self.methods.clans_of_clans_and_tag(kwargs)
        current_war_response = await self.clan_war.current_war(clan_and_tag[1])
        if current_war_response == {"reason": "notFound"}:
            raise InvalidClanTag
        if current_war_response['state'] != 'notInWar':
            warlog_json = await self.clan_war.war_log(clan_and_tag[1])
            warlog_json_opponent = await self.clan_war.war_log(current_war_response['opponent']['tag'].strip('#'))
            clans_list = (
                (await self.clan.clan(clan_and_tag[1]),
                 [war_clan for war_clan in warlog_json['items'] if war_clan['attacksPerMember'] == 2][:20]),
                (await self.clan.clan(current_war_response['opponent']['tag'].strip('#')),
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
        await ctx.send(f"The clan **{clan_and_tag[0]}** (#{clan_and_tag[1]}) is not in a clan war.")

    async def lineup(self, ctx: CommandContext, kwargs) -> None:
        clan_and_tag = self.methods.clans_of_clans_and_tag(kwargs)
        current_war_response = await self.clan_war.current_war(clan_and_tag[1])
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
            clan_member_list = await self.player.player_bulk(clan_member_tag_list)
            clan_max_name_len = len(max([member['name'] for member in clan_member_list], key=len))
            opponent_member_list = await self.player.player_bulk(opponent_member_tag_list)
            opponent_max_name_len = len(max([member['name'] for member in opponent_member_list], key=len))
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
        await ctx.send(f"The clan **{clan_and_tag[0]}** (#{clan_and_tag[1]}) is not in a clan war.")
