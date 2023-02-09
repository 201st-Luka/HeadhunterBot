import aiohttp
from Bot.Variables import clashOfClansHeaders


async def current_war(clan_tag: str):
    session = aiohttp.ClientSession()
    response = await session.get(
        f"https://api.clashofclans.com/v1/clans/%23{clan_tag}/currentwar",
        headers=clashOfClansHeaders
    )
    await session.close()
    return await response.json()


async def war_log(clan_tag: str):
    session = aiohttp.ClientSession()
    response = await session.get(
        f"https://api.clashofclans.com/v1/clans/%23{clan_tag}/warlog",
        headers=clashOfClansHeaders
    )
    await session.close()
    return await response.json()
