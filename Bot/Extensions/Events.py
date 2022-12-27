import logging

from interactions import Extension, Client, extension_listener, ClientPresence, StatusType, PresenceActivity, PresenceActivityType

from Database.Data_base import DataBase
from Database.User import User


class Events(Extension):
    client: Client
    user: User = User(DataBase())

    def __init__(self, client: Client):
        self.client = client
        return

    @extension_listener(name="on_start")
    async def on_start(self):
        await self.client.change_presence(ClientPresence(
            status=StatusType.ONLINE,
            activities=[
                PresenceActivity(
                    name="in development...",
                    type=PresenceActivityType.GAME
                )
            ]
        ))
        logging.info("The bot started.")
        return

    @extension_listener(name="on_ready")
    async def on_ready(self):
        logging.info(f"Successfully logged in as {self.client.me.name} ({self.client.me.id})")
        guilds_bot_is_on = self.client.guilds
        guild_ids = self.user.guilds.fetch_guild_ids()
        for guild in guilds_bot_is_on:
            if guild.id not in guild_ids:
                self.user.guilds.insert_guild(guild.id, guild_name=str(guild.name))
        return


def setup(client: Client):
    Events(client)
    return
