import asyncio
from typing import Any, Coroutine
from urllib.parse import quote

import aiohttp

from Bot.variables import Variables


class ClanWar:
    def __init__(self):
        self.variables = Variables()

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    def current_war(self, clan_tag: str) -> Coroutine[Any, Any, None] | None:
        async def get_current_war(clan_tag: str) -> None:
            async with self:
                async with await self.session.get(f"https://api.clashofclans.com/v1/clans/{quote(clan_tag)}/currentwar",
                                                  headers=self.variables.clash_of_clans_headers) as response:
                    return await response.json()

        if asyncio.get_running_loop() is None:
            return asyncio.run(get_current_war(clan_tag))
        return get_current_war(clan_tag)

    def war_log(self, clan_tag: str) -> Coroutine[Any, Any, None] | None:
        async def get_war_log(clan_tag: str) -> None:
            async with self:
                async with await self.session.get(f"https://api.clashofclans.com/v1/clans/{quote(clan_tag)}/warlog",
                                                  headers=self.variables.clash_of_clans_headers) as response:
                    return await response.json()

        if asyncio.get_running_loop() is None:
            return asyncio.run(get_war_log(clan_tag))
        return get_war_log(clan_tag)
