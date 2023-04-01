import asyncio
from typing import Any, Coroutine

import aiohttp

from Bot.variables import Variables


class Leagues:
    def __init__(self):
        self.variables = Variables()

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    def league(self, league_id: int) -> Coroutine[Any, Any, None] | None:
        async def get_league(league_id: int) -> None:
            async with self:
                async with await self.session.get(url=f"https://api.clashofclans.com/v1/leagues/{str(league_id)}",
                                                  headers=self.variables.clash_of_clans_headers) as response:
                    return await response.json()

        if asyncio.get_running_loop() is None:
            return asyncio.run(get_league(league_id))
        return get_league(league_id)

    def leagues(self) -> Coroutine[Any, Any, None] | None:
        async def get_leagues() -> None:
            async with self:
                async with await self.session.get(url="https://api.clashofclans.com/v1/leagues",
                                                  headers=self.variables.clash_of_clans_headers) as response:
                    return await response.json()

        if asyncio.get_running_loop() is None:
            return asyncio.run(get_leagues())
        return get_leagues()

    def leagues_seasons(self, league_id: int, season_id: int, limit: int = 100) -> Coroutine[Any, Any, None] | None:
        async def get_leagues_seasons(league_id: int, season_id: int, limit: int = 100) -> None:
            async with self:
                async with await self.session.get(
                        url=f"https://api.clashofclans.com/v1/leagues/{str(league_id)}/seasons/{str(season_id)}?limit={str(limit)}",
                        headers=self.variables.clash_of_clans_headers) as response:
                    return await response.json()

        if asyncio.get_running_loop() is None:
            return asyncio.run(get_leagues_seasons(league_id, season_id, limit))
        return get_leagues_seasons(league_id, season_id, limit)

    def leagues_seasons_after(self, league_id: int, season_id: int, after: str, limit: int = 100) -> Coroutine[Any, Any, None] | None:
        async def get_leagues_seasons_after(league_id: int, season_id: int, after: str, limit: int = 100) -> None:
            async with self:
                async with await self.session.get(
                        url=f"https://api.clashofclans.com/v1/leagues/{str(league_id)}/seasons/{str(season_id)}?limit={str(limit)}&after={after}",
                        headers=self.variables.clash_of_clans_headers) as response:
                    return await response.json()

        if asyncio.get_running_loop() is None:
            return asyncio.run(get_leagues_seasons_after(league_id, season_id, after, limit))
        return get_leagues_seasons_after(league_id, season_id, after, limit)

    def leagues_seasons_before(self, league_id: int, season_id: int, before: str, limit: int = 100) -> Coroutine[Any, Any, None] | None:
        async def get_leagues_seasons_after(league_id: int, season_id: int, before: str, limit: int = 100) -> None:
            async with self:
                async with await self.session.get(
                        url=f"https://api.clashofclans.com/v1/leagues/{str(league_id)}/seasons/{str(season_id)}?limit={str(limit)}&before={before}",
                        headers=self.variables.clash_of_clans_headers) as response:
                    return await response.json()

        if asyncio.get_running_loop() is None:
            return asyncio.run(get_leagues_seasons_after(league_id, season_id, before, limit))
        return get_leagues_seasons_after(league_id, season_id, before, limit)

    def league_seasons(self, league_id: int) -> Coroutine[Any, Any, None] | None:
        async def get_league_seasons(league_id: int) -> None:
            async with self:
                async with await self.session.get(
                        url=f"https://api.clashofclans.com/v1/leagues/{str(league_id)}/seasons",
                        headers=self.variables.clash_of_clans_headers) as response:
                    return await response.json()

        if asyncio.get_running_loop() is None:
            return asyncio.run(get_league_seasons(league_id))
        return get_league_seasons(league_id)
