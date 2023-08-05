import interactions
from interactions import Snowflake

from Database import DataBase, DataBaseLogger


Table = "guild_blacklist"


def create_table(db: DataBase):
    db.cursor.execute(
        "CREATE TABLE guild_blacklist ("
        "id INTEGER PRIMARY KEY,"
        "guild_id INTEGER,"
        "player_tag TEXT,"
        "player_name TEXT,"
        "reason TEXT"
        ");"
    )
    db.save_changes()

    DataBaseLogger.logger.info(f"Created table {Table}.")

    return


class TableGuildBlacklist:
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
        return

    @DataBaseLogger()
    def insert_player(self, guild_id: Snowflake, player_tag: str, player_name: str, reason: str) -> None:
        self.cursor.execute("INSERT INTO guild_blacklist(guild_id, player_tag, player_name, reason) VALUES (?,?,?,?);",
                            (guild_id, player_tag, player_name, reason))
        self.__db.save_changes()
        return

    @DataBaseLogger()
    def remove_player(self, guild_id: Snowflake, player_tag: str) -> None:
        self.cursor.execute("DELETE FROM guild_blacklist WHERE guild_id=? AND player_tag=?;",
                            (guild_id, player_tag))
        self.__db.save_changes()
        return

    @DataBaseLogger()
    def fetch_players(self, guild_id: Snowflake) -> list[tuple[str, str, str | None]]:
        self.cursor.execute("SELECT player_tag, player_name, reason FROM guild_blacklist WHERE guild_id=?;",
                            (guild_id,))
        return self.cursor.fetchall()

    @DataBaseLogger()
    def fetch_all(self):
        self.cursor.execute("SELECT * FROM guild_blacklist;")
        return self.cursor.fetchall()
