import aiohttp
from Bot.Variables import clashOfClansHeaders


async def current_league_group(clan_tag: str):
    session = aiohttp.ClientSession()
    response = await session.get(
        f"https://api.clashofclans.com/v1/clans/%23{clan_tag}/currentwar/leaguegroup",
        headers=clashOfClansHeaders
    )
    await session.close()
    return await response.json()


async def league_war(war_tag: str):
    session = aiohttp.ClientSession()
    response = await session.get(
        f"https://api.clashofclans.com/v1/clanwarleagues/wars/%23{war_tag}",
        headers=clashOfClansHeaders
    )
    await session.close()
    return await response.json()
