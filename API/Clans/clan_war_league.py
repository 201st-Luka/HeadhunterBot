import asyncio
from typing import Any, Coroutine

import aiohttp

from Bot.variables import Variables


class ClanWarLeague:
    def __init__(self):
        self.variables = Variables()

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    def current_league_group(self, clan_tag: str) -> Coroutine[Any, Any, None] | None:
        async def get_current_league_group(clan_tag: str) -> None:
            async with self:
                async with await self.session.get(
                        f"https://api.clashofclans.com/v1/clans/%23{clan_tag}/currentwar/leaguegroup",
                        headers=self.variables.clash_of_clans_headers) as response:
                    return await response.json()

        if asyncio.get_running_loop() is None:
            return asyncio.run(get_current_league_group(clan_tag))
        return get_current_league_group(clan_tag)

    async def league_war(self, war_tag: str) -> Coroutine[Any, Any, None] | None:
        async def get_league_war(war_tag: str) -> None:
            async with self:
                async with await self.session.get(f"https://api.clashofclans.com/v1/clanwarleagues/wars/%23{war_tag}",
                                                  headers=self.variables.clash_of_clans_headers) as response:
                    return await response.json()

        if asyncio.get_running_loop() is None:
            return asyncio.run(get_league_war(war_tag))
        return get_league_war(war_tag)
