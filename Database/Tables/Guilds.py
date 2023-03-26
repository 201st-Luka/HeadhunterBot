import logging
from interactions import Snowflake

from Database.Data_base import DataBase
from Bot.Databaselogger import database_logger


class Guilds:
    table = "guilds"
    __db = None
    cursor = None
    connection = None

    def __init__(self, database: DataBase):
        self.cursor = database.get_cursor()
        self.connection = database.get_connection()
        self.__db = database

    @database_logger
    def insert_guild(self,
                     guild_id: Snowflake,
                     guild_name: str = None,
                     guild_owner: Snowflake = None,
                     clan_tag: str = None,
                     clan_name: str = None,
                     feed_channel: Snowflake = None,
                     warlog_channel: Snowflake = None,
                     clantable_channel: Snowflake = None,
                     time_zone=None):
        self.cursor.execute(
            "INSERT INTO guilds VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);",
            (str(guild_id), guild_name, str(guild_owner), clan_tag, clan_name, str(feed_channel), str(warlog_channel), str(clantable_channel), time_zone)
        )
        logging.info(f"Inserted entry '{guild_name}' in the database.")
        self.__db.save_changes()
        return

    @database_logger
    def delete_guild(self, guild_id: Snowflake):
        self.cursor.execute("DELETE FROM guilds WHERE guild_id=?;",
                            (str(guild_id),))
        self.__db.save_changes()
        return

    @database_logger
    def fetch_guild(self, guild_id: Snowflake):
        self.cursor.execute("SELECT * FROM guilds WHERE guild_id=?;",
                            (str(guild_id),))
        return self.cursor.fetchone()

    @database_logger
    def fetch_all(self):
        self.cursor.execute("SELECT * FROM guilds;")
        return self.cursor.fetchall()

    @database_logger
    def fetch_guild_ids(self):
        self.cursor.execute("SELECT DISTINCT guild_id FROM guilds;")
        return [guild_id[0] for guild_id in self.cursor.fetchall()]

    @database_logger
    def fetch_clan_tags(self):
        self.cursor.execute("SELECT DISTINCT clan_tag FROM guilds;")
        return [clan_tag[0] for clan_tag in self.cursor.fetchall()]

    @database_logger
    def fetch_clantag(self, guild_id: Snowflake):
        self.cursor.execute("SELECT clan_tag FROM guilds WHERE guild_id=?;",
                            (str(guild_id),))
        return self.cursor.fetchone()[0]

    @database_logger
    def fetch_clantags(self, guild_id: Snowflake) -> tuple:
        self.cursor.execute("SELECT clan_tag FROM guilds WHERE guild_id=?;",
                            (str(guild_id),))
        return tuple(clan_tag[0] for clan_tag in self.cursor.fetchall())

    @database_logger
    def fetch_clanname_and_tag(self, guild_id: Snowflake):
        self.cursor.execute("SELECT clan_name, clan_tag FROM guilds WHERE guild_id=?;",
                            (str(guild_id),))
        return self.cursor.fetchone()

    @database_logger
    def update_clan_tag_and_name(self, guild_id: Snowflake, clan_tag: str | None, clan_name: str | None):
        self.cursor.execute("UPDATE guilds SET clan_tag=?, clan_name=? WHERE guild_id=?;",
                            (clan_tag, clan_name, str(guild_id)))
        self.__db.save_changes()
        return

    def update_clan_tag(self, guild_id: Snowflake, clan_tag: str | None):
        self.cursor.execute("UPDATE guilds SET clan_tag=? WHERE guild_id=?;",
                            (clan_tag, str(guild_id)))
        self.__db.save_changes()
        return
