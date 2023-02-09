import aiohttp
from Bot.Variables import clashOfClansHeaders


async def clan(location_id: int, limit: int = 100):
    session = aiohttp.ClientSession()
    response = await session.get(
        url=f"https://api.clashofclans.com/v1/locations/{str(location_id)}/rankings/clans?limit={str(limit)}",
        headers=clashOfClansHeaders
    )
    await session.close()
    return await response.json()

async def clan_after(location_id: int, after: str, limit: int = 100):
    session = aiohttp.ClientSession()
    response = await session.get(
        url=f"https://api.clashofclans.com/v1/locations/{str(location_id)}/rankings/clans?limit={str(limit)}&after={after}",
        headers=clashOfClansHeaders
    )
    await session.close()
    return await response.json()

async def clan_before(location_id: int, before: str, limit: int = 100):
    session = aiohttp.ClientSession()
    response = await session.get(
        url=f"https://api.clashofclans.com/v1/locations/{str(location_id)}/rankings/clans?limit={str(limit)}&before={before}",
        headers=clashOfClansHeaders
    )
    await session.close()
    return await response.json()

async def clan_versus(location_id: int, limit: int = 100):
    session = aiohttp.ClientSession()
    response = await session.get(
        url=f"https://api.clashofclans.com/v1/locations/{str(location_id)}/rankings/clans-versus?limit={str(limit)}",
        headers=clashOfClansHeaders
    )
    await session.close()
    return await response.json()

async def clan_versus_after(location_id: int, after: str, limit: int = 100):
    session = aiohttp.ClientSession()
    response = await session.get(
        url=f"https://api.clashofclans.com/v1/locations/{str(location_id)}/rankings/clans-versus?limit={str(limit)}&after={after}",
        headers=clashOfClansHeaders
    )
    await session.close()
    return await response.json()

async def clan_versus_before(location_id: int, before: str, limit: int = 100):
    session = aiohttp.ClientSession()
    response = await session.get(
        url=f"https://api.clashofclans.com/v1/locations/{str(location_id)}/rankings/clans-versus?limit={str(limit)}&before={before}",
        headers=clashOfClansHeaders
    )
    await session.close()
    return await response.json()
