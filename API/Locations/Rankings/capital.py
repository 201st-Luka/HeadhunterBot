import asyncio
from typing import Any, Coroutine

import aiohttp

from Bot.variables import Variables


class Capital:
    def __init__(self):
        self.session = aiohttp.ClientSession()
        self.variables = Variables()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

    def capital(self, location_id: int, limit: int = 100) -> Coroutine[Any, Any, None] | None:
        async def get_capital(location_id: int, limit: int = 100) -> None:
            async with self:
                async with await self.session.get(
                        url=f"https://api.clashofclans.com/v1/locations/{str(location_id)}/rankings/capitals?limit={str(limit)}",
                        headers=self.variables.clash_of_clans_headers) as response:
                    return await response.json()

        if asyncio.get_running_loop() is None:
            return asyncio.run(get_capital(location_id, limit))
        return get_capital(location_id, limit)

    def capital_after(self, location_id: int, after: str, limit: int = 100) -> Coroutine[Any, Any, None] | None:
        async def get_capital_after(location_id: int, after: str, limit: int = 100) -> None:
            async with self:
                async with await self.session.get(
                        url=f"https://api.clashofclans.com/v1/locations/{str(location_id)}/rankings/capitals?limit={str(limit)}&after={after}",
                        headers=self.variables.clash_of_clans_headers) as response:
                    return await response.json()

        if asyncio.get_running_loop() is None:
            return asyncio.run(get_capital_after(location_id, after, limit))
        return get_capital_after(location_id, after, limit)

    def capital_before(self, location_id: int, before: str, limit: int = 100) -> Coroutine[Any, Any, None] | None:
        async def get_capital_before(location_id: int, before: str, limit: int = 100) -> None:
            async with self:
                async with await self.session.get(
                        url=f"https://api.clashofclans.com/v1/locations/{str(location_id)}/rankings/capitals?limit={str(limit)}&before={before}",
                        headers=self.variables.clash_of_clans_headers) as response:
                    return await response.json()

        if asyncio.get_running_loop() is None:
            return asyncio.run(get_capital_before(location_id, before, limit))
        return get_capital_before(location_id, before, limit)
