import interactions

from Database.Database import DataBase, DataBaseLogger


class TableMessages:
    table = "messages"
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
    def insert_message(self, message_id: interactions.Snowflake, message_type=None, type_value=None,
                       message_time_stamp=None, tag=None):
        with open(f'Database/Queries/json_messages.txt') as json_file:
            self.cursor.execute(json_file.read())
            self.__db.save_changes()
            self.__db.logger.info(f"Inserted entry '{message_id}' of table 'messages' in the database.")

    @DataBaseLogger()
    def update_message(self, message_id: interactions.Snowflake, message_type=None, type_value=None,
                       message_time_stamp=None):
        self.cursor.execute("SELECT * FROM messages WHERE message_id=?", (str(message_id),))
        old_message = self.cursor.fetchone()
        if message_type is None:
            message_type = old_message[1]
        if type_value is None:
            type_value = old_message[2]
        if message_time_stamp is None:
            message_time_stamp = old_message[3]
        self.cursor.execute("UPDATE messages SET message_type=?, type_value=?, message_time_stamp=? WHERE message_id=?",
                            (message_type, str(type_value), message_time_stamp, str(message_id)))
        self.__db.save_changes()

    @DataBaseLogger()
    def fetch_message(self, message_id: interactions.Snowflake):
        self.cursor.execute("SELECT * FROM messages WHERE message_id=?", (str(message_id),))
        return self.cursor.fetchone()

    @DataBaseLogger()
    def fetch_type_value(self, message_id: interactions.Snowflake):
        self.cursor.execute("SELECT type_value FROM messages WHERE message_id=?", (str(message_id),))
        return self.cursor.fetchone()[0]

    @DataBaseLogger()
    def fetch_tag(self, message_id: interactions.Snowflake):
        self.cursor.execute("SELECT tag FROM messages WHERE message_id=?", (str(message_id),))
        return self.cursor.fetchone()[0]

    @DataBaseLogger()
    def fetch_all(self):
        self.cursor.execute("SELECT * FROM messages")
        return self.cursor.fetchall()
