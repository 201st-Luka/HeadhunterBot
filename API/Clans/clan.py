import asyncio
from asyncio import gather
from typing import Iterable, Any, Coroutine
from urllib.parse import urlencode, quote

import aiohttp

from Bot.variables import Variables


class Clan:
    def __init__(self):
        self.variables = Variables()

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    def clan_search(self, name: str, limit: int, war_frequency: str = None, location_id: int = None,
                    min_members: int = None, max_members: int = None, min_clan_points: int = None,
                    min_clan_level: int = None, after: str = None, before: str = None, label_ids: str = None):
        async def get_clan_search(name: str, limit: int, war_frequency: str = None, location_id: int = None,
                                  min_members: int = None, max_members: int = None, min_clan_points: int = None,
                                  min_clan_level: int = None, after: str = None, before: str = None,
                                  label_ids: str = None):
            async with self:
                params = urlencode(
                    {'name': name,
                     'limit': limit}
                )
                async with await self.session.get(f"https://api.clashofclans.com/v1/clans?{params}",
                                                  headers=self.variables.clash_of_clans_headers) as response:
                    return await response.json()

        if asyncio.get_running_loop() is None:
            return asyncio.run(get_clan_search(name, limit, war_frequency, location_id,
                                               min_members, max_members, min_clan_points,
                                               min_clan_level, after, before, label_ids))
        return get_clan_search(name, limit, war_frequency, location_id, min_members, max_members, min_clan_points,
                               min_clan_level, after, before, label_ids)

    def clan(self, clan_tag: str) -> Coroutine[Any, Any, None] | None:
        async def get_clan(clan_tag: str) -> None:
            async with self:
                async with await self.session.get(f"https://api.clashofclans.com/v1/clans/{quote(clan_tag)}",
                                                  headers=self.variables.clash_of_clans_headers) as response:
                    return await response.json()

        if asyncio.get_running_loop() is None:
            return asyncio.run(get_clan(clan_tag))
        return get_clan(clan_tag)

    def clan_bulk(self, clan_list: Iterable[str]) -> list[Any] | Coroutine[Any, Any, list[Any]]:
        async def get_clan_bulk(clan_list: Iterable[str]) -> list[Any]:
            async with self:
                tasks = [self.session.get(f"https://api.clashofclans.com/v1/clans/{quote(clan_tag)}",
                                          headers=self.variables.clash_of_clans_headers) for clan_tag in clan_list]
                responses = await gather(*tasks)
                return [await response.json() for response in responses]

        if asyncio.get_running_loop() is None:
            return asyncio.run(get_clan_bulk(clan_list))
        return get_clan_bulk(clan_list)

    def members(self, clan_tag: str) -> Coroutine[Any, Any, None] | None:
        async def get_members(clan_tag: str) -> None:
            async with self:
                async with await self.session.get(f"https://api.clashofclans.com/v1/clans/{quote(clan_tag)}/members",
                                                  headers=self.variables.clash_of_clans_headers) as response:
                    return await response.json()

        if asyncio.get_running_loop() is None:
            return asyncio.run(get_members(clan_tag))
        return get_members(clan_tag)
