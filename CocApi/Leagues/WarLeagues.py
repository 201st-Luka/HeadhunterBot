import aiohttp
from Bot.Variables import clashOfClansHeaders


async def war_leagues():
    session = aiohttp.ClientSession()
    response = await session.get(
        url="https://api.clashofclans.com/v1/warleagues",
        headers=clashOfClansHeaders
    )
    await session.close()
    return await response.json()

async def war_league(league_id: int):
    session = aiohttp.ClientSession()
    response = await session.get(
        url=f"https://api.clashofclans.com/v1/warleagues/{league_id}",
        headers=clashOfClansHeaders
    )
    await session.close()
    return await response.json()
