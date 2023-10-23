from abc import ABC
from sqlite3 import Cursor

from ..database import DataBase


class AbcTable(ABC):
    name: str = None
    create_table_query: str = None

    @classmethod
    def create_table(cls, db: DataBase):
        db.cursor.execute(cls.create_table_query)
        db.save_changes()

        return

    def __init__(self, database: DataBase = None):
        if database is None:
            database = DataBase()
        self.cursor: Cursor = database.cursor
        self.connection = database.connection
        self._db = database
