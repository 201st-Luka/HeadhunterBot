import aiohttp
from Bot.Variables import clashOfClansHeaders


def clan_search(name: str, warFrequency: str = None, locationId: int = None, minMembers: int = None,
                maxMembers: int = None, minClanPoints: int = None, minClanLevel: int = None, limit: int = None,
                after: str = None, before: str = None, labelIds: str = None):
    return


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
