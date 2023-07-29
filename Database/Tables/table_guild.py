from os import path, getcwd

from interactions import Snowflake

from Database import DataBase, DataBaseLogger


Table = "guilds"


def create_table(db: DataBase):
    db.cursor.execute(
        "CREATE TABLE guilds ("
        "guild_id INTEGER,"
        "guild_name TEXT,"
        "guild_owner INTEGER,"
        "clan_tag TEXT,"
        "clan_name TEXT,"
        "feed_channel INTEGER,"
        "warlog_channel INTEGER,"
        "clantable_channel INTEGER,"
        "time_zone TEXT"
        ");"
    )
    db.save_changes()

    DataBaseLogger.logger.info(f"Created table {Table}.")

    return


class TableGuilds:
    table = Table
    __db = None
    cursor = None
    connection = None

    def __init__(self, database: DataBase = None):
        if database is None:
            database = DataBase()
        self.cursor = database.cursor
        self.connection = database.connection
        self.__db = database

    @DataBaseLogger()
    def insert_guild(self, guild_id: int, guild_name: str = None, guild_owner: int = None,
                     clan_tag: str = None, clan_name: str = None, feed_channel: int = None,
                     warlog_channel: int = None, clantable_channel: int = None, time_zone=None):
        self.cursor.execute("INSERT INTO guilds VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);",
                            (guild_id, guild_name, guild_owner, clan_tag, clan_name, feed_channel, warlog_channel,
                             clantable_channel, time_zone)
                            )
        self.__db.logger.info(f"Inserted entry '{guild_name}' of table 'guilds' in the database.")
        self.__db.save_changes()

    @DataBaseLogger()
    def delete_guild(self, guild_id: Snowflake):
        self.cursor.execute("DELETE FROM guilds WHERE guild_id=?;", (guild_id,))
        self.__db.save_changes()

    @DataBaseLogger()
    def fetch_guild(self, guild_id: Snowflake) -> tuple:
        self.cursor.execute("SELECT * FROM guilds WHERE guild_id=?;", (guild_id,))
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
        self.cursor.execute("SELECT clan_tag FROM guilds WHERE guild_id=?;", (guild_id,))
        return self.cursor.fetchone()[0]

    @DataBaseLogger()
    def fetch_feed_channel(self, guild_id: Snowflake) -> None | int:
        self.cursor.execute("SELECT feed_channel FROM guilds WHERE guild_id=?;", (guild_id,))
        return self.cursor.fetchone()[0]

    @DataBaseLogger()
    def fetch_clanname_and_tag(self, guild_id: Snowflake):
        self.cursor.execute("SELECT clan_name, clan_tag FROM guilds WHERE guild_id=?;", (guild_id,))
        return self.cursor.fetchone()

    @DataBaseLogger()
    def update_clan_tag_and_name(self, guild_id: Snowflake, clan_tag: str | None, clan_name: str | None):
        self.cursor.execute("UPDATE guilds SET clan_tag=?, clan_name=? WHERE guild_id=?;",
                            (clan_tag, clan_name, guild_id))
        self.__db.save_changes()

    @DataBaseLogger()
    def update_clan_tag(self, guild_id: Snowflake, clan_tag: str | None):
        self.cursor.execute("UPDATE guilds SET clan_tag=? WHERE guild_id=?;", (clan_tag, guild_id))
        self.__db.save_changes()

    @DataBaseLogger()
    def update_feed_channel(self, guild_id: Snowflake, channel_id: Snowflake) -> None:
        self.cursor.execute("UPDATE guilds SET feed_channel=? WHERE guild_id=?;", (channel_id, guild_id))
        self.__db.save_changes()
