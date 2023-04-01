import asyncio
from typing import Any, Coroutine

import aiohttp

from Bot.variables import Variables


class Players:
    def __init__(self):
        self.session = aiohttp.ClientSession()
        self.variables = Variables()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

    def player(self, location_id: int, limit: int = 100) -> Coroutine[Any, Any, None] | None:
        async def get_player(location_id: int, limit: int = 100) -> None:
            async with self:
                async with await self.session.get(
                        url=f"https://api.clashofclans.com/v1/locations/{str(location_id)}/rankings/players?limit={str(limit)}",
                        headers=self.variables.clash_of_clans_headers) as response:
                    return await response.json()

        if asyncio.get_running_loop() is None:
            return asyncio.run(get_player(location_id, limit))
        return get_player(location_id, limit)

    def player_after(self, location_id: int, after: str, limit: int = 100) -> Coroutine[Any, Any, None] | None:
        async def get_player_after(location_id: int, after: str, limit: int = 100) -> None:
            async with self:
                async with await self.session.get(
                        url=f"https://api.clashofclans.com/v1/locations/{str(location_id)}/rankings/players?limit={str(limit)}&after={after}",
                        headers=self.variables.clash_of_clans_headers) as response:
                    return await response.json()

        if asyncio.get_running_loop() is None:
            return asyncio.run(get_player_after(location_id, after, limit))
        return get_player_after(location_id, after, limit)

    def player_before(self, location_id: int, before: str, limit: int = 100) -> Coroutine[Any, Any, None] | None:
        async def get_player_before(location_id: int, before: str, limit: int = 100) -> None:
            async with self:
                async with await self.session.get(
                        url=f"https://api.clashofclans.com/v1/locations/{str(location_id)}/rankings/players?limit={str(limit)}&before={before}",
                        headers=self.variables.clash_of_clans_headers) as response:
                    return await response.json()

        if asyncio.get_running_loop() is None:
            return asyncio.run(get_player_before(location_id, before, limit))
        return get_player_before(location_id, before, limit)

    def player_versus(self, location_id: int, limit: int = 100) -> Coroutine[Any, Any, None] | None:
        async def get_player_versus(location_id: int, limit: int = 100) -> None:
            async with self:
                async with await self.session.get(
                        url=f"https://api.clashofclans.com/v1/locations/{str(location_id)}/rankings/players-versus?limit={str(limit)}",
                        headers=self.variables.clash_of_clans_headers) as response:
                    return await response.json()

        if asyncio.get_running_loop() is None:
            return asyncio.run(get_player_versus(location_id, limit))
        return get_player_versus(location_id, limit)

    def player_versus_after(self, location_id: int, after: str, limit: int = 100) -> Coroutine[Any, Any, None] | None:
        async def get_player_versus_after(location_id: int, after: str, limit: int = 100) -> None:
            async with self:
                async with await self.session.get(
                        url=f"https://api.clashofclans.com/v1/locations/{str(location_id)}/rankings/players-versus?limit={str(limit)}&after={after}",
                        headers=self.variables.clash_of_clans_headers) as response:
                    return await response.json()

        if asyncio.get_running_loop() is None:
            return asyncio.run(get_player_versus_after(location_id, after, limit))
        return get_player_versus_after(location_id, after, limit)

    def player_versus_before(self, location_id: int, before: str, limit: int = 100) -> Coroutine[Any, Any, None] | None:
        async def get_player_versus_after(location_id: int, before: str, limit: int = 100) -> None:
            async with self:
                async with await self.session.get(
                        url=f"https://api.clashofclans.com/v1/locations/{str(location_id)}/rankings/players-versus?limit={str(limit)}&before={before}",
                        headers=self.variables.clash_of_clans_headers) as response:
                    return await response.json()

        if asyncio.get_running_loop() is None:
            return asyncio.run(get_player_versus_after(location_id, before, limit))
        return get_player_versus_after(location_id, before, limit)
