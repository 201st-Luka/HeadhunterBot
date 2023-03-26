import asyncio
import aiohttp
import json
from Bot.Variables import clashOfClansHeaders
from urllib.parse import quote


async def player(player_tag: str):
    session = aiohttp.ClientSession()
    response = await session.get(
        f"https://api.clashofclans.com/v1/players/{quote(player_tag)}",
        headers=clashOfClansHeaders
    )
    await session.close()
    return await response.json()


async def player_bulk(player_list: list[str]):
    session = aiohttp.ClientSession()
    tasks = [
        session.get(
            f"https://api.clashofclans.com/v1/players/{quote(player_tag)}",
            headers=clashOfClansHeaders
        ) for player_tag in player_list
    ]
    responses = await asyncio.gather(*tasks)
    await session.close()
    return [await response.json() for response in responses]


async def verify_token(player_tag: str, token: str):
    session = aiohttp.ClientSession()
    response = await session.post(
        f"https://api.clashofclans.com/v1/players/%23{player_tag}/verifytoken",
        headers=clashOfClansHeaders,
        data=json.dumps({"token": token})
    )
    await session.close()
    return await response.json()
