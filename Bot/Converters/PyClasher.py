from interactions import BaseContext, Converter
from pyclasher import ClanRequest, PlayerRequest, ClanMembersRequest, ClanSearchRequest
from pyclasher.models import ApiCodes

from Bot.Exceptions import InvalidPlayerTag, InvalidClanTag
from Database.user import User


class ClanConverter(Converter):
    async def convert(self, ctx: BaseContext, clan_str: str) -> None | list[ClanRequest]:
        db_user = User()

        clans: list[str] = []

        if clan_str is not None:
            clans.append(clan_str)

            clans += [clan.tag for clan in await ClanSearchRequest(name=clan_str, limit=100).request()]

        if guild_clan_tag := db_user.guilds.fetch_clantag(ctx.guild_id) is not None:
            clans.append(guild_clan_tag)

        if not len(clans):
            return None

        return [ClanRequest(clan) for clan in clans if clan.startswith("#")]


class PlayerConverter(Converter):
    async def convert(self, ctx: BaseContext, player_str: str) -> None | list[PlayerRequest]:
        db_user = User()

        players: list[str] = []

        if player_str is not None:
            players.append(player_str)

        if len(accounts := db_user.users.fetch_player_tags(ctx.author.id)):
            players += accounts

        if clan := db_user.guilds.fetch_clantag(ctx.guild_id) is not None:
            try:
                clan_members = await ClanMembersRequest(clan).request()
            except ApiCodes.NOT_FOUND:
                pass
            else:
                players += [member.tag for member in clan_members if player_str in member.tag or player_str in member.name]

        if not len(players):
            return None

        return [PlayerRequest(player) for player in players if player.startswith("#")]


class ClanTagConverter(Converter):
    async def convert(self, ctx: BaseContext, clan_tag: None | str) -> ClanRequest:
        if clan_tag is None:
            raise InvalidClanTag

        try:
            clan = await ClanRequest(clan_tag).request()
        except ApiCodes.NOT_FOUND:
            raise InvalidClanTag
        else:
            return clan


class PlayerTagConverter(Converter):
    async def convert(self, ctx: BaseContext, player_tag: None | str) -> PlayerRequest:
        if player_tag is None:
            raise InvalidPlayerTag

        try:
            player = await PlayerRequest(player_tag).request()
        except ApiCodes.NOT_FOUND:
            raise InvalidPlayerTag
        else:
            return player
