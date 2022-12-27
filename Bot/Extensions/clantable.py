import datetime

from interactions import Extension, Client, extension_command, Option, OptionType, Choice, CommandContext, Embed, ActionRow, Button, ButtonStyle

from Bot.Extensions.Extensionssetup import extension_command_wrapper
from Bot.Methods import check_clan_tag
from CocApi.Clans.Clan import clan
from CocApi.Players.PLayer import player_bulk
from Database.User import User
from Database.Data_base import DataBase


class ClanTableCommand(Extension):
    client: Client
    user: User = User(DataBase())

    def __init__(self, client: Client):
        self.client = client
        return

    @extension_command(
        name="clantable",
        description="returns clan member information",
        default_scope=True,
        options=[
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
            ),
            Option(
                name="clan_tag",
                description="enter your clantag here",
                type=OptionType.STRING,
                required=False
            )
        ]
    )
    @extension_command_wrapper
    async def clantable(self, ctx: CommandContext, clan_tag=None, sort="0", order=""):
        clan_tag = check_clan_tag(clan_tag, ctx, self.user)
        response_clan = clan(clan_tag)
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
                    url=f"https://cocp.it/clan/{clan_tag}"
                ), Button(
                    style=ButtonStyle.LINK,
                    label=f"{response_clan['name']} on ClashOfStats",
                    url=f"https://www.clashofstats.com/clans/{clan_tag}/summary"
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
        print(case)
        await first_message.edit("".join((
            "`#    name", (max_name_len - 2) * ' ', "trophies  war  stars  donations  received  th  role       level  tag",
            (max_tag_len - 3) * ' ', "`\n",
            *(item for outer_list in members_table_str[0:10] for item in outer_list))))
        if case:
            for i in range(1, case + 1):
                await ctx.channel.send("".join(item for outer_list in members_table_str[i * 10:(i + 1) * 10] for item in outer_list))
        return


def setup(client: Client):
    ClanTableCommand(client)
    return
