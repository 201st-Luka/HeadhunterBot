import asyncio
from typing import Any, Coroutine

import aiohttp

from Bot.variables import Variables


class WarLeagues:
    def __init__(self):
        self.variables = Variables()

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    def war_league(self) -> Coroutine[Any, Any, None] | None:
        async def get_war_league() -> None:
            async with self:
                async with await self.session.get(url="https://api.clashofclans.com/v1/warleagues",
                                                  headers=self.variables.clash_of_clans_headers) as response:
                    return await response.json()

        if asyncio.get_running_loop() is None:
            return asyncio.run(get_war_league())
        return get_war_league()

    async def war_leagues(self, league_id: int) -> Coroutine[Any, Any, None] | None:
        async def get_war_leagues(league_id: int) -> None:
            async with self:
                async with await self.session.get(url=f"https://api.clashofclans.com/v1/warleagues/{league_id}",
                                                  headers=self.variables.clash_of_clans_headers) as response:
                    return await response.json()

        if asyncio.get_running_loop() is None:
            return asyncio.run(get_war_leagues(league_id))
        return get_war_leagues(league_id)
