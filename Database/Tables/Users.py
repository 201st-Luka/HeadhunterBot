from interactions import Snowflake

from Bot.Databaselogger import database_logger
from Database.Data_base import DataBase


class Users:
    table = "users"
    __db = None
    cursor = None
    connection = None

    def __init__(self, database: DataBase):
        self.cursor = database.get_cursor()
        self.connection = database.get_connection()
        self.__db = database

    @database_logger
    def insert_user(self, user_id: Snowflake, player_tag: str, player_name: str):
        self.cursor.execute("INSERT INTO users(user_id, player_tag, player_name) VALUES (?, ?, ?)",
                            (str(user_id), player_tag, player_name))
        self.__db.save_changes()
        return

    @database_logger
    def delete_user_player(self, user_id: Snowflake, player_tag: str):
        self.cursor.execute("DELETE FROM users WHERE user_id=? AND player_tag=?;",
                            (str(user_id), player_tag))
        self.__db.save_changes()
        return

    @database_logger
    def fetch_user(self, user_id: Snowflake):
        self.cursor.execute("SELECT * FROM users WHERE user_id=?",
                            (str(user_id),))
        return self.cursor.fetchone()

    @database_logger
    def fetch_all(self):
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()

    @database_logger
    def fetch_user_ids(self):
        self.cursor.execute("SELECT DISTINCT user_id FROM users")
        return tuple(user_id[0] for user_id in self.cursor.fetchall())

    @database_logger
    def fetch_player_tags(self, user_id: Snowflake):
        self.cursor.execute("SELECT player_tag FROM users WHERE user_id=?",
                            (str(user_id),))
        return tuple(player_tag[0] for player_tag in self.cursor.fetchall())

    @database_logger
    def update_player_tag(self, user_id: Snowflake, player_tag: str):
        self.cursor.execute("UPDATE users SET player_tag=? WHERE user_id=?",
                            (player_tag, str(user_id)))
        self.__db.save_changes()
        return

    @database_logger
    def fetch_players(self, user_id: Snowflake):
        self.cursor.execute("SELECT player_name, player_tag FROM users WHERE user_id=?",
                            (str(user_id),))
        return self.cursor.fetchall()

    @database_logger
    def fetch_all_player_tags(self):
        self.cursor.execute("SELECT DISTINCT player_tag FROM users")
        return tuple(player_tag[0] for player_tag in self.cursor.fetchall())

    @database_logger
    def fetch_all_players_of_user(self, user_id: Snowflake) -> list[tuple]:
        self.cursor.execute("SELECT player_name, player_tag FROM users WHERE user_id=?",
                            (str(user_id),))
        return self.cursor.fetchall()

    @database_logger
    def fetch_user_player_tag_name(self, user_id: Snowflake, player_tag: str):
        self.cursor.execute("SELECT player_name FROM users WHERE user_id=? AND player_tag=?",
                            (str(user_id), player_tag))
        return self.cursor.fetchone()

