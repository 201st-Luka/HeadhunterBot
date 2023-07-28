from interactions import Snowflake

from Database import DataBase, DataBaseLogger


Table = "users"


def create_table(db: DataBase):
    db.cursor.execute(
        "CREATE TABLE users ("
        "user_id INTEGER PRIMARY KEY,"
        "player_tag TEXT,"
        "player_name TEXT"
        ");"
    )
    db.save_changes()

    DataBaseLogger.logger.info(f"Created table {Table}.")

    return


class TableUsers:
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
    def insert_user(self, user_id: Snowflake, player_tag: str, player_name: str):
        self.cursor.execute("INSERT INTO users(user_id, player_tag, player_name) VALUES (?, ?, ?)",
                            (str(user_id), player_tag, player_name))
        self.__db.save_changes()

    @DataBaseLogger()
    def delete_user_player(self, user_id: Snowflake, player_tag: str):
        self.cursor.execute("DELETE FROM users WHERE user_id=? AND player_tag=?;", (str(user_id), player_tag))
        self.__db.save_changes()

    @DataBaseLogger()
    def fetch_user(self, user_id: Snowflake):
        self.cursor.execute("SELECT * FROM users WHERE user_id=?", (str(user_id),))
        return self.cursor.fetchone()

    @DataBaseLogger()
    def fetch_all(self) -> list:
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()

    @DataBaseLogger()
    def fetch_user_ids(self) -> list:
        self.cursor.execute("SELECT DISTINCT user_id FROM users")
        return self.cursor.fetchall()

    @DataBaseLogger()
    def fetch_player_tags(self, user_id: Snowflake) -> list:
        self.cursor.execute("SELECT player_tag FROM users WHERE user_id=?", (str(user_id),))
        return self.cursor.fetchall()

    @DataBaseLogger()
    def update_player_tag(self, user_id: Snowflake, player_tag: str):
        self.cursor.execute("UPDATE users SET player_tag=? WHERE user_id=?", (player_tag, str(user_id)))
        self.__db.save_changes()

    @DataBaseLogger()
    def fetch_all_player_tags(self) -> list:
        self.cursor.execute("SELECT DISTINCT player_tag FROM users")
        return self.cursor.fetchall()

    @DataBaseLogger()
    def fetch_all_players_of_user(self, user_id: Snowflake) -> list[tuple]:
        self.cursor.execute("SELECT player_name, player_tag FROM users WHERE user_id=?", (str(user_id),))
        return self.cursor.fetchall()

    @DataBaseLogger()
    def fetch_user_player_tag_name(self, user_id: Snowflake, player_tag: str) -> list:
        self.cursor.execute("SELECT player_name FROM users WHERE user_id=? AND player_tag=?", (str(user_id), player_tag))
        return self.cursor.fetchone()
