import aiohttp
from Bot.Variables import clashOfClansHeaders


async def player_labels():
    session = aiohttp.ClientSession()
    response = await session.get(
        url="https://api.clashofclans.com/v1/labels/clans",
        headers=clashOfClansHeaders
    )
    await session.close()
    return await response.json()
