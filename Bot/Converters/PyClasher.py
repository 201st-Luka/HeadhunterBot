from interactions import BaseContext, Converter
from pyclasher import ClanRequest, PlayerRequest

from Bot.HeadhunterBot import HeadhunterClient


class ClanConverter(Converter):
    async def convert(self, ctx: BaseContext, clan_tag: None | str) -> None | ClanRequest:
        client: HeadhunterClient = ctx.client

        if clan_tag is None:
            clan_tag = client.db_user.guilds.fetch_clantag(ctx.guild_id)

            if clan_tag is None:
                return None

        return ClanRequest(clan_tag)


class PlayerConverter(Converter):
    async def convert(self, ctx: BaseContext, player_tag: str | None) -> None | list[PlayerRequest]:
        client: HeadhunterClient = ctx.client

        player_tags: list[str] = []

        if player_tag is not None:
            player_tags.append(player_tag)

        accounts: list = client.db_user.users.fetch_player_tags(ctx.author)

        if len(accounts):
            player_tags += accounts

        if not len(player_tags):
            return None

        return [PlayerRequest(player) for player in player_tags if player.startswith("#")]
