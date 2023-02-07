from Database.User import User
from Database.Data_base import DataBase


class DbInstance:
    def __init__(self):
        self.db = DataBase()
        self.user = User(self.db)
        return

    def close_db(self):
        self.db.close()