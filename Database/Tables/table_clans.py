from Database.Database import DataBase


class TableClans:
    table = "clans"
    __db = None
    cursor = None
    connection = None

    def __init__(self, database: DataBase = None):
        if database is None:
            database = DataBase()
        self.cursor = database.get_cursor()
        self.connection = database.get_connection()
        self.__db = database
