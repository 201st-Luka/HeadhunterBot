import requests
from Bot import clashOfClansHeaders


def current_league_group(clan_tag: str):
    return requests.get(
        f"https://api.clashofclans.com/v1/clans/%23{clan_tag}/currentwar/leaguegroup",
        headers=clashOfClansHeaders
    ).json()


def league_war(war_tag: str):
    return requests.get(
        f"https://api.clashofclans.com/v1/clanwarleagues/wars/%23{war_tag}",
        headers=clashOfClansHeaders
    ).json()
