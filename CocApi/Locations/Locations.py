import aiohttp
from Bot.Variables import clashOfClansHeaders


async def locations():
    session = aiohttp.ClientSession()
    response = await session.get(
        url="https://api.clashofclans.com/v1/locations",
        headers=clashOfClansHeaders
    )
    await session.close()
    return await response.json()

async def location(location_id: int):
    session = aiohttp.ClientSession()
    response = await session.get(
        url=f"https://api.clashofclans.com/v1/locations/{str(location_id)}",
        headers=clashOfClansHeaders
    )
    await session.close()
    return await response.json()
