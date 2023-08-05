from Database import DataBase, DataBaseLogger

Table = "clans"


def create_table(db: DataBase):
    db.cursor.execute(
        "CREATE TABLE clans ("
        "id INTEGER PRIMARY KEY,"
        "clan TEXT"
        ");"
    )
    db.save_changes()

    DataBaseLogger.logger.info(f"Created table {Table}.")

    return


class TableClans:
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
