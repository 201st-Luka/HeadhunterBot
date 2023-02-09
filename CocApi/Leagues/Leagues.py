import aiohttp
from Bot.Variables import clashOfClansHeaders


async def leagues():
    session = aiohttp.ClientSession()
    response = await session.get(
        url="https://api.clashofclans.com/v1/leagues",
        headers=clashOfClansHeaders
    )
    await session.close()
    return await response.json()

async def leagues_seasons(league_id: int, season_id: int, limit: int = 100):
    session = aiohttp.ClientSession()
    response = await session.get(
        url=f"https://api.clashofclans.com/v1/leagues/{str(league_id)}/seasons/{str(season_id)}?limit={str(limit)}",
        headers=clashOfClansHeaders
    )
    await session.close()
    return await response.json()

async def leagues_seasons_after(league_id: int, season_id: int, after:str, limit: int = 100):
    session = aiohttp.ClientSession()
    response = await session.get(
        url=f"https://api.clashofclans.com/v1/leagues/{str(league_id)}/seasons/{str(season_id)}?limit={str(limit)}&after={after}",
        headers=clashOfClansHeaders
    )
    await session.close()
    return await response.json()

async def leagues_seasons_before(league_id: int, season_id: int, before:str, limit: int = 100):
    session = aiohttp.ClientSession()
    response = await session.get(
        url=f"https://api.clashofclans.com/v1/leagues/{str(league_id)}/seasons/{str(season_id)}?limit={str(limit)}&after={before}",
        headers=clashOfClansHeaders
    )
    await session.close()
    return await response.json()

async def league(league_id: int):
    session = aiohttp.ClientSession()
    response = await session.get(
        url=f"https://api.clashofclans.com/v1/leagues/{str(league_id)}",
        headers=clashOfClansHeaders
    )
    await session.close()
    return await response.json()

async def league_seasons(league_id: int):
    session = aiohttp.ClientSession()
    response = await session.get(
        url=f"https://api.clashofclans.com/v1/leagues/29000022{str(league_id)}/seasons",
        headers=clashOfClansHeaders
    )
    await session.close()
    return await response.json()

