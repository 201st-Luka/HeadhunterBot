from interactions import Snowflake

from .abc import AbcTable


class TableUsers(AbcTable):
    name = "users"
    create_table_query = (
        "CREATE TABLE users ("
        "id INTEGER PRIMARY KEY,"
        "user_id INTEGER,"
        "player_tag TEXT,"
        "player_name TEXT"
        ");"
    )

    def insert_user(self, user_id: Snowflake, player_tag: str, player_name: str) -> None:
        self.cursor.execute("INSERT INTO users(user_id, player_tag, player_name) VALUES (?, ?, ?);",
                            (user_id, player_tag, player_name))
        self._db.save_changes()

    def delete_user_player(self, user_id: Snowflake, player_tag: str):
        self.cursor.execute("DELETE FROM users WHERE user_id=? AND player_tag=?;", (user_id, player_tag))
        self._db.save_changes()

    def fetch_user(self, user_id: Snowflake):
        self.cursor.execute("SELECT * FROM users WHERE user_id=?;", (user_id,))
        return self.cursor.fetchone()

    def fetch_all(self) -> list:
        self.cursor.execute("SELECT * FROM users;")
        return self.cursor.fetchall()

    def fetch_user_ids(self) -> list:
        self.cursor.execute("SELECT DISTINCT user_id FROM users;")
        return self.cursor.fetchall()

    def fetch_player_tags(self, user_id: Snowflake) -> tuple[str, ...]:
        self.cursor.execute("SELECT player_tag FROM users WHERE user_id=?;", (user_id,))
        return tuple(tag[0] for tag in self.cursor.fetchall())

    def update_player_tag(self, user_id: Snowflake, player_tag: str):
        self.cursor.execute("UPDATE users SET player_tag=? WHERE user_id=?;", (player_tag, user_id))
        self._db.save_changes()

    def fetch_all_player_tags(self) -> list:
        self.cursor.execute("SELECT DISTINCT player_tag FROM users;")
        return self.cursor.fetchall()

    def fetch_all_players_of_user(self, user_id: Snowflake) -> list[tuple]:
        self.cursor.execute("SELECT player_name, player_tag FROM users WHERE user_id=?;", (user_id,))
        return self.cursor.fetchall()

    def fetch_user_player_tag_name(self, user_id: Snowflake, player_tag: str) -> list:
        self.cursor.execute("SELECT player_name FROM users WHERE user_id=? AND player_tag=?;", (user_id, player_tag))
        return self.cursor.fetchone()
