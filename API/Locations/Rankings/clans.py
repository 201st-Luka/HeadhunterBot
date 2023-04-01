import asyncio
from typing import Any, Coroutine

import aiohttp

from Bot.variables import Variables


class Clans:
    def __init__(self):
        self.session = aiohttp.ClientSession()
        self.variables = Variables()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

    async def clan(self, location_id: int, limit: int = 100) -> Coroutine[Any, Any, None] | None:
        async def get_clan(location_id: int, limit: int = 100) -> None:
            async with self:
                async with await self.session.get(
                        url=f"https://api.clashofclans.com/v1/locations/{str(location_id)}/rankings/clans?limit={str(limit)}",
                        headers=self.variables.clash_of_clans_headers) as response:
                    return await response.json()

        if asyncio.get_running_loop() is None:
            return asyncio.run(get_clan(location_id, limit))
        return get_clan(location_id, limit)

    async def clan_after(self, location_id: int, after: str, limit: int = 100) -> Coroutine[Any, Any, None] | None:
        async def get_clan_after(location_id: int, after: str, limit: int = 100) -> None:
            async with self:
                async with await self.session.get(
                        url=f"https://api.clashofclans.com/v1/locations/{str(location_id)}/rankings/clans?limit={str(limit)}&after={after}",
                        headers=self.variables.clash_of_clans_headers) as response:
                    return await response.json()

        if asyncio.get_running_loop() is None:
            return asyncio.run(get_clan_after(location_id, after, limit))
        return get_clan_after(location_id, after, limit)

    async def clan_before(self, location_id: int, before: str, limit: int = 100) -> Coroutine[Any, Any, None] | None:
        async def get_clan_before(location_id: int, before: str, limit: int = 100) -> None:
            async with self:
                async with await self.session.get(
                        url=f"https://api.clashofclans.com/v1/locations/{str(location_id)}/rankings/clans?limit={str(limit)}&before={before}",
                        headers=self.variables.clash_of_clans_headers) as response:
                    return await response.json()

        if asyncio.get_running_loop() is None:
            return asyncio.run(get_clan_before(location_id, before, limit))
        return get_clan_before(location_id, before, limit)

    async def clan_versus(self, location_id: int, limit: int = 100) -> Coroutine[Any, Any, None] | None:
        async def get_clan_versus(location_id: int, limit: int = 100) -> None:
            async with self:
                async with await self.session.get(
                        url=f"https://api.clashofclans.com/v1/locations/{str(location_id)}/rankings/clans-versus?limit={str(limit)}",
                        headers=self.variables.clash_of_clans_headers) as response:
                    return await response.json()

        if asyncio.get_running_loop() is None:
            return asyncio.run(get_clan_versus(location_id, limit))
        return get_clan_versus(location_id, limit)

    async def clan_versus_after(self, location_id: int, after: str, limit: int = 100) -> Coroutine[Any, Any, None] | None:
        async def get_clan_versus_after(location_id: int, after: str, limit: int = 100) -> None:
            async with self:
                async with await self.session.get(
                        url=f"https://api.clashofclans.com/v1/locations/{str(location_id)}/rankings/clans-versus?limit={str(limit)}&after={after}",
                        headers=self.variables.clash_of_clans_headers) as response:
                    return await response.json()

        if asyncio.get_running_loop() is None:
            return asyncio.run(get_clan_versus_after(location_id, after, limit))
        return get_clan_versus_after(location_id, after, limit)

    async def clan_versus_before(self, location_id: int, before: str, limit: int = 100) -> Coroutine[Any, Any, None] | None:
        async def get_clan_versus_before(location_id: int, before: str, limit: int = 100) -> None:
            async with self:
                async with await self.session.get(
                        url=f"https://api.clashofclans.com/v1/locations/{str(location_id)}/rankings/clans-versus?limit={str(limit)}&before={before}",
                        headers=self.variables.clash_of_clans_headers) as response:
                    return await response.json()

        if asyncio.get_running_loop() is None:
            return asyncio.run(get_clan_versus_before(location_id, before, limit))
        return get_clan_versus_before(location_id, before, limit)
