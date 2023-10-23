from interactions import Snowflake

from .abc import AbcTable


class TableGuildBlacklist(AbcTable):
    name = "guild_blacklist"
    create_table_query = (
        "CREATE TABLE guild_blacklist ("
        "id INTEGER PRIMARY KEY,"
        "guild_id INTEGER,"
        "player_tag TEXT,"
        "player_name TEXT,"
        "reason TEXT"
        ");"
    )

    def insert_player(self, guild_id: Snowflake, player_tag: str, player_name: str, reason: str) -> None:
        self.cursor.execute("INSERT INTO guild_blacklist(guild_id, player_tag, player_name, reason) VALUES (?,?,?,?);",
                            (guild_id, player_tag, player_name, reason))
        self._db.save_changes()
        return

    def remove_player(self, guild_id: Snowflake, player_tag: str) -> None:
        self.cursor.execute("DELETE FROM guild_blacklist WHERE guild_id=? AND player_tag=?;",
                            (guild_id, player_tag))
        self._db.save_changes()
        return

    def fetch_players(self, guild_id: Snowflake) -> list[tuple[str, str, str | None]]:
        self.cursor.execute("SELECT player_tag, player_name, reason FROM guild_blacklist WHERE guild_id=?;",
                            (guild_id,))
        return self.cursor.fetchall()

    def fetch_all(self):
        self.cursor.execute("SELECT * FROM guild_blacklist;")
        return self.cursor.fetchall()
