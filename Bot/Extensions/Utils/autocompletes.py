from interactions import CommandContext, Choice

from CocApi.Clans.Clan import members, clan, clan_search, clan_bulk
from CocApi.Clans.Clanwar import current_war
from CocApi.Players.Player import player
from Database.User import User


async def player_tag_auto_complete(
        ctx: CommandContext,
        user: User,
        input_player_tag: str = None
) -> None:
    """
    :param ctx: CommandContext
    :param user: User
    :param input_player_tag: str = None
    :return: None
    """
    choices = []
    clan_tag = user.guilds.fetch_clantag(ctx.guild_id)
    if clan_tag is not None:
        choices = [
            Choice(
                name=f"{member['name']} {member['tag']} {'Leader' if member['role'] == 'leader' else 'Co-leader' if member['role'] == 'coLeader' else 'Elder' if member['role'] == 'admin' else 'Member'}",
                value=member['tag']
            ) for member in (await members(clan_tag))['items']
            if input_player_tag in member['name'] or input_player_tag.upper() in member['tag']
        ]
    if input_player_tag is not None:
        if input_player_tag[0] != '#':
            input_player_tag = "".join(('#', input_player_tag))
        player_response = await player(input_player_tag)
        if 'reason' not in player_response:
            choice = Choice(
                name=f"{player_response['name']} {player_response['tag']} {'Leader' if player_response['role'] == 'leader' else 'Co-leader' if player_response['role'] == 'coLeader' else 'Elder' if player_response['role'] == 'admin' else 'Member'}",
                value=player_response['tag']
            )
            if not len(choices):
                choices = [choice]
            else:
                choices.insert(0, choice)
    await ctx.populate([
        elem for i, elem in enumerate(choices)
        if (elem.name, elem.value) not in [(ch.name, ch.value) for ch in choices[:i]]
    ][:25])
    return


async def player_auto_complete(
        ctx: CommandContext,
        user: User,
        input_player: str = None
) -> None:
    """

    :param ctx: CommandContext
    :param user: User
    :param input_player: str = ""
    :return: None
    """
    players = user.users.fetch_all_players_of_user(ctx.user.id)
    if len(players) == 0:
        await ctx.populate([])
        return
    if input_player is None:
        choices = [
            Choice(
                name=f"{player_[0]} {player_[1]}",
                value=player_[1]
            ) for player_ in players
        ]
    else:
        choices = [
            Choice(
                name=f"{player_[0]} {player_[1]}",
                value=player_[1]
            ) for player_ in players
            if input_player in player_[0] or input_player.upper() in player_[1]
        ]
    await ctx.populate(choices[0:25])
    return


async def clan_tag_auto_complete(
        ctx: CommandContext,
        user: User,
        input_clan_tag: str = None
) -> None:
    clan_tag = user.guilds.fetch_clantag(ctx.guild_id)
    choices = []
    if clan_tag is not None:
        clan_response = await clan(clan_tag)
        if 'reason' not in clan_response:
            choices.append(Choice(
                name=f"{clan_response['name']} {clan_response['tag']}, "
                     f"Lvl: {clan_response['clanLevel']}, "
                     f"Location: {clan_response['location']['name']}, "
                     f"{clan_response['members']}/50",
                value=str(clan_response['tag'])
            ))
            war_response = await current_war(clan_tag)
            if war_response['state'] != 'notInWar':
                opponent = await clan(war_response['opponent']['tag'])
                if 'reason' not in opponent:
                    choices.append(Choice(
                        name=f"{opponent['name']} {opponent['tag']}, "
                             f"Lvl: {opponent['clanLevel']}, "
                             f"Location: {opponent['location']['name']}, "
                             f"{opponent['members']}/50",
                        value=str(opponent['tag'])
                    ))
        if input_clan_tag is not None:
            input_copy = "".join(('#', input_clan_tag)) if not input_clan_tag.startswith('#') else input_clan_tag
            input_response = await clan(input_copy)
            if 'reason' not in input_response:
                choices.append(Choice(
                    name=f"{input_response['name']} {input_response['tag']}, "
                         f"Lvl: {input_response['clanLevel']}, "
                         f"Location: {input_response['location']['name']}, "
                         f"{input_response['members']}/50",
                    value=str(input_response['tag'])
                ))
            if len(input_clan_tag) > 3:
                search_choices = [
                    Choice(
                        name=f"{item['name']} {item['tag']}, "
                             f"Lvl: {item['clanLevel']}, "
                             f"Location: {item['location']['name']}, "
                             f"{item['members']}/50",
                        value=str(item['tag'])
                    ) for item in (await clan_search(input_clan_tag, limit=25))['items']
                ]
                choices += search_choices
    await ctx.populate([
        elem for i, elem in enumerate(choices)
        if (elem.name, elem.value) not in [(ch.name, ch.value) for ch in choices[:i]]
    ][:25])
    return


async def clan_auto_complete(
        ctx: CommandContext,
        user: User,
        input_clan: str = None
) -> None:
    clan_tags = user.guilds.fetch_clantags(ctx.guild_id)
    if len(clan_tags) == 0:
        await ctx.populate([])
        return
    choices = [Choice(
        name=c_response
    ) for c_response in await clan_bulk(clan_tags)]

    if input_clan is None:
        choices = [
            elem for i, elem in enumerate(choices)
            if (elem.name, elem.value) not in [(ch.name, ch.value) for ch in choices[:i]]
        ][:25]
    else:
        choices = [
            elem for i, elem in enumerate(choices)
            if (elem.name, elem.value) not in [
                (ch.name, ch.value) for ch in choices[:i]
            ] and input_clan in elem.name or input_clan in elem.value
        ][:25]
    await ctx.populate(choices)
    return

