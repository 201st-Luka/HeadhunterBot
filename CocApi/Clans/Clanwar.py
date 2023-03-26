import aiohttp
from Bot.Variables import clashOfClansHeaders
from urllib.parse import quote


async def current_war(clan_tag: str):
    session = aiohttp.ClientSession()
    response = await session.get(
        f"https://api.clashofclans.com/v1/clans/{quote(clan_tag)}/currentwar",
        headers=clashOfClansHeaders
    )
    await session.close()
    return await response.json()


async def war_log(clan_tag: str):
    session = aiohttp.ClientSession()
    response = await session.get(
        f"https://api.clashofclans.com/v1/clans/{quote(clan_tag)}/warlog",
        headers=clashOfClansHeaders
    )
    await session.close()
    return await response.json()
