import requests
from Bot.Variables import clashOfClansHeaders


def current_war(clan_tag: str):
    return requests.get(
        f"https://api.clashofclans.com/v1/clans/%23{clan_tag}/currentwar",
        headers=clashOfClansHeaders
    ).json()


def war_log(clan_tag: str, limit: int = 20, after: str = None, before: str = None):
    return requests.get(
        f"https://api.clashofclans.com/v1/clans/%23{clan_tag}/warlog",
        headers=clashOfClansHeaders
    ).json()
