from interactions import BaseContext, Converter
from pyclasher import ClanRequest, PlayerRequest

from Database.user import User


class ClanConverter(Converter):
    async def convert(self, ctx: BaseContext, clan_tag: None | str) -> None | list[ClanRequest]:
        db_user = User()

        clans: list[str] = []

        if clan_tag is not None:
            clans.append(clan_tag)

        if guild_clan_tag := db_user.guilds.fetch_clantag(ctx.guild_id) is not None:
            clans.append(guild_clan_tag)

        if not len(clans):
            return None

        return [ClanRequest(clan) for clan in clans]


class PlayerConverter(Converter):
    async def convert(self, ctx: BaseContext, player_tag: None | str) -> None | list[PlayerRequest]:
        db_user = User()

        players: list[str] = []

        if player_tag is not None:
            players.append(player_tag)

        if len(accounts := db_user.users.fetch_player_tags(ctx.author.id)):
            players += accounts

        if not len(players):
            return None

        return [PlayerRequest(player) for player in players if player.startswith("#")]
