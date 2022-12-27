import requests
import json
from Bot.Variables import clashOfClansHeaders


def player(player_tag: str):
    return requests.get(
        "https://api.clashofclans.com/v1/players/%23" + player_tag,
        headers=clashOfClansHeaders
    ).json()


def player_bulk(player_list: list[str]):
    session = requests.Session()
    return [
        session.get(
            "https://api.clashofclans.com/v1/players/%23" + player_tag,
            headers=clashOfClansHeaders
        ).json() for player_tag in player_list
    ]


def verify_token(player_tag: str, token: str):
    return requests.post(
        f"https://api.clashofclans.com/v1/players/%23{player_tag}/verifytoken",
        headers=clashOfClansHeaders,
        data=json.dumps({"token": token})
    ).json()
