import aiohttp
from Bot.Variables import clashOfClansHeaders


async def get_url_image(image_url: str):
    session = aiohttp.ClientSession()

    response = await session.get(
        url=image_url,
        headers=clashOfClansHeaders
    )
    await session.close()
    return response
