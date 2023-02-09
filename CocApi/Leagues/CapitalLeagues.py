import aiohttp
from Bot.Variables import clashOfClansHeaders

async def capital_leagues():
    session = aiohttp.ClientSession()
    response = await session.get(
        url="https://api.clashofclans.com/v1/capitalleagues",
        headers=clashOfClansHeaders
    )
    await session.close()
    return await response.json()

async def capital_leagues_league(league_id: int):
    session = aiohttp.ClientSession()
    response = await session.get(
        url=f"https://api.clashofclans.com/v1/capitalleagues/{str(league_id)}",
        headers=clashOfClansHeaders
    )
    await session.close()
    return await response.json()

