import requests
from Bot.Variables import clashOfClansHeaders


def clan_search(name: str, warFrequency: str = None, locationId: int = None, minMembers: int = None,
                maxMembers: int = None, minClanPoints: int = None, minClanLevel: int = None, limit: int = None,
                after: str = None, before: str = None, labelIds: str = None):
    return


def clan(clan_tag: str):
    return requests.get(
        f"https://api.clashofclans.com/v1/clans/%23{clan_tag}",
        headers=clashOfClansHeaders
    ).json()


def members(clan_tag: str):
    return requests.get(
        f"https://api.clashofclans.com/v1/clans/%23{clan_tag}/members",
        headers=clashOfClansHeaders
    ).json()


def get_url_image(image_url: str):
    return requests.get(
        image_url,
        headers=clashOfClansHeaders
    )
