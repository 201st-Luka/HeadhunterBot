import asyncio
import json
from typing import Any, Coroutine
from urllib.parse import quote

import aiohttp

from Bot.variables import Variables


class Player:
    def __init__(self):
        self.variables = Variables()

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    def player(self, player_tag: str) -> Coroutine[Any, Any, None] | None:
        async def get_player(player_tag: str) -> None:
            async with self:
                async with await self.session.get(f"https://api.clashofclans.com/v1/players/{quote(player_tag)}",
                                                  headers=self.variables.clash_of_clans_headers) as response:
                    return await response.json()

        if asyncio.get_running_loop() is None:
            return asyncio.run(get_player(player_tag))
        return get_player(player_tag)

    def player_bulk(self, player_list: list[str]) -> list[Any] | Coroutine[Any, Any, list[Any]]:
        async def get_player_bulk(player_list: list[str]) -> list[Any]:
            async with self:
                tasks = [self.session.get(f"https://api.clashofclans.com/v1/players/{quote(player_tag)}",
                                          headers=self.variables.clash_of_clans_headers) for player_tag in player_list]
                responses = await asyncio.gather(*tasks)
                return [await response.json() for response in responses]

        if asyncio.get_running_loop() is None:
            return asyncio.run(get_player_bulk(player_list))
        return get_player_bulk(player_list)

    def verify_token(self, player_tag: str, token: str) -> Coroutine[Any, Any, None] | None:
        async def get_verify_token(player_tag: str, token: str) -> None:
            async with self:
                async with await self.session.post(
                        f"https://api.clashofclans.com/v1/players/%23{player_tag}/verifytoken",
                        headers=self.variables.clash_of_clans_headers, data=json.dumps({"token": token})) as response:
                    return await response.json()

        if asyncio.get_running_loop() is None:
            return asyncio.run(get_verify_token(player_tag, token))
        return get_verify_token(player_tag, token)
