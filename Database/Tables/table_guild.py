from os import path, getcwd

from interactions import Snowflake

from Database.Database import DataBase, DataBaseLogger


class TableGuilds:
    table = "guilds"
    __db = None
    cursor = None
    connection = None

    def __init__(self, database: DataBase = None):
        if database is None:
            database = DataBase()
        self.cursor = database.get_cursor()
        self.connection = database.get_connection()
        self.__db = database

    @DataBaseLogger()
    def insert_guild(self, guild_id: int, guild_name: str = None, guild_owner: int = None,
                     clan_tag: str = None, clan_name: str = None, feed_channel: int = None,
                     warlog_channel: int = None, clantable_channel: int = None, time_zone=None):
        self.cursor.execute("INSERT INTO guilds VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);",
                            (str(guild_id), guild_name, str(guild_owner), clan_tag, clan_name, str(feed_channel), str(warlog_channel), str(clantable_channel), time_zone)
                            )
        self.__db.logger.info(f"Inserted entry '{guild_name}' of table 'guilds' in the database.")
        self.__db.save_changes()

    @DataBaseLogger()
    def delete_guild(self, guild_id: Snowflake):
        self.cursor.execute("DELETE FROM guilds WHERE guild_id=?;", (str(guild_id),))
        self.__db.save_changes()

    @DataBaseLogger()
    def fetch_guild(self, guild_id: Snowflake) -> tuple:
        self.cursor.execute("SELECT * FROM guilds WHERE guild_id=?;", (str(guild_id),))
        return self.cursor.fetchone()

    @DataBaseLogger()
    def fetch_all(self) -> list[tuple]:
        self.cursor.execute("SELECT * FROM guilds;")
        return self.cursor.fetchall()

    @DataBaseLogger()
    def fetch_guild_ids(self) -> list:
        self.cursor.execute("SELECT DISTINCT guild_id FROM guilds;")
        return [guild_id for guild_id, *rest in self.cursor.fetchall()]

    @DataBaseLogger()
    def fetch_clan_tags(self) -> list:
        self.cursor.execute("SELECT DISTINCT clan_tag FROM guilds;")
        return self.cursor.fetchall()

    @DataBaseLogger()
    def fetch_clantag(self, guild_id: Snowflake) -> None | str:
        self.cursor.execute("SELECT clan_tag FROM guilds WHERE guild_id=?;", (str(guild_id),))
        return self.cursor.fetchone()

    @DataBaseLogger()
    def fetch_clantags(self, guild_id: Snowflake) -> list:
        self.cursor.execute("SELECT clan_tag FROM guilds WHERE guild_id=?;", (str(guild_id),))
        return self.cursor.fetchall()

    @DataBaseLogger()
    def fetch_clanname_and_tag(self, guild_id: Snowflake):
        self.cursor.execute("SELECT clan_name, clan_tag FROM guilds WHERE guild_id=?;", (str(guild_id),))
        return self.cursor.fetchone()

    @DataBaseLogger()
    def update_clan_tag_and_name(self, guild_id: Snowflake, clan_tag: str | None, clan_name: str | None):
        self.cursor.execute("UPDATE guilds SET clan_tag=?, clan_name=? WHERE guild_id=?;", (clan_tag, clan_name, str(guild_id)))
        self.__db.save_changes()

    @DataBaseLogger()
    def update_clan_tag(self, guild_id: Snowflake, clan_tag: str | None):
        self.cursor.execute("UPDATE guilds SET clan_tag=? WHERE guild_id=?;", (clan_tag, str(guild_id)))
        self.__db.save_changes()
