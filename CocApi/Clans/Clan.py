import aiohttp
from Bot.Variables import clashOfClansHeaders
from urllib.parse import urlencode


async def clan_search(name: str, limit: int, warFrequency: str = None, locationId: int = None, minMembers: int = None,
                maxMembers: int = None, minClanPoints: int = None, minClanLevel: int = None,
                after: str = None, before: str = None, labelIds: str = None):
    session = aiohttp.ClientSession()
    params = urlencode(
        {
            'name': name,
            'limit': limit
        }
    )
    response = await session.get(
        f"https://api.clashofclans.com/v1/clans?{params}",
        headers=clashOfClansHeaders
    )
    await session.close()
    return await response.json()


async def clan(clan_tag: str):
    session = aiohttp.ClientSession()
    response = await session.get(
        f"https://api.clashofclans.com/v1/clans/%23{clan_tag}",
        headers=clashOfClansHeaders
    )
    await session.close()
    return await response.json()


async def members(clan_tag: str):
    session = aiohttp.ClientSession()
    response = await session.get(
        f"https://api.clashofclans.com/v1/clans/%23{clan_tag}/members",
        headers=clashOfClansHeaders
    )
    await session.close()
    return await response.json()
