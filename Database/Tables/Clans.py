from Database.Data_base import DataBase


class Clans:
    table = "clans"
    __db = None
    cursor = None
    connection = None

    def __init__(self, database: DataBase):
        self.cursor = database.get_cursor()
        self.connection = database.get_connection()
        self.__db = database
