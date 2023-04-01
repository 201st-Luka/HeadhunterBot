import asyncio
from typing import Any, Coroutine

import aiohttp

from Bot.variables import Variables


class CapitalLeagues:
    def __init__(self):
        self.variables = Variables()

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    def capital_leagues(self) -> Coroutine[Any, Any, None] | None:
        async def get_capital_leagues() -> None:
            async with self:
                async with await self.session.get(url="https://api.clashofclans.com/v1/capitalleagues",
                                                  headers=self.variables.clash_of_clans_headers) as response:
                    return await response.json()

        if asyncio.get_running_loop() is None:
            return asyncio.run(get_capital_leagues())
        return get_capital_leagues()

    def capital_leagues_league(self, league_id: int) -> Coroutine[Any, Any, None] | None:
        async def get_capital_leagues_league(league_id: int) -> None:
            async with self:
                async with await self.session.get(
                        url=f"https://api.clashofclans.com/v1/capitalleagues/{str(league_id)}",
                        headers=self.variables.clash_of_clans_headers) as response:
                    return await response.json()

        if asyncio.get_running_loop() is None:
            return asyncio.run(get_capital_leagues_league(league_id))
        return get_capital_leagues_league(league_id)
