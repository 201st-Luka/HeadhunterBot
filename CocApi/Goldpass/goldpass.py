import aiohttp
from Bot.Variables import clashOfClansHeaders


async def goldpass():
    session = aiohttp.ClientSession()
    response = await session.get(
        url="https://api.clashofclans.com/v1/goldpass/seasons/current",
        headers=clashOfClansHeaders
    )
    await session.close()
    return await response.json()
