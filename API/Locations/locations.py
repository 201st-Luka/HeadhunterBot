import asyncio
from typing import Any, Coroutine

import aiohttp

from Bot.variables import Variables


class ClashOfClansAPI:
    def __init__(self):
        self.variables = Variables()

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    def locations(self) -> Coroutine[Any, Any, None] | None:
        async def get_locations() -> None:
            async with self:
                async with await self.session.get(url="https://api.clashofclans.com/v1/locations",
                                                  headers=self.variables.clash_of_clans_headers) as response:
                    return await response.json()

        if asyncio.get_running_loop() is None:
            return asyncio.run(get_locations())
        return get_locations()

    def location(self, location_id: int) -> Coroutine[Any, Any, None] | None:
        async def get_location(location_id: int) -> None:
            async with self:
                async with await self.session.get(url=f"https://api.clashofclans.com/v1/locations/{str(location_id)}",
                                                  headers=self.variables.clash_of_clans_headers) as response:
                    return await response.json()

        if asyncio.get_running_loop() is None:
            return asyncio.run(get_location(location_id))
        return get_location(location_id)
