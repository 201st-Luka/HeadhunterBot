import asyncio
from typing import Any, Coroutine

import aiohttp

from Bot.variables import Variables


class GoldPass:
    def __init__(self):
        self.variables = Variables()

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    def goldpass(self) -> Coroutine[Any, Any, None] | None:
        async def get_goldpass() -> None:
            async with self:
                async with await self.session.get(url="https://api.clashofclans.com/v1/goldpass/seasons/current",
                                                  headers=self.variables.clash_of_clans_headers) as response:
                    return await response.json()

        if asyncio.get_running_loop() is None:
            return asyncio.run(get_goldpass())
        return get_goldpass()
