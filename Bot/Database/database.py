from logging import Logger
from sqlite3 import connect

# from .Tables import (TableGuilds, TableGuildBlacklist, TablePlayers, TableUsers, TableClans)


# Tables = [TableGuilds, TableGuildBlacklist, TablePlayers, TableUsers, TableClans]


class DataBase:
    __instance: "DataBase" = None

    def __new__(cls, db_path: str = None, logger: Logger = None) -> "DataBase":
        if db_path is None and logger is None and cls.__instance is None:
            raise AttributeError("db_path and logger must be different from None for the first initialisation.")
        if cls.__instance is None:
            logger.info("Creating new DataBase instance")
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @property
    def instance(self) -> "DataBase":
        return DataBase.__instance

    def __init__(self, db_path: str = None, logger: Logger = None) -> None:
        if db_path is not None and logger is not None:
            self.logger = logger.getChild("Db")
            self.logger.info("Initialising the Database")
            self.path = db_path
            self.__db = connect(self.path)
            self.__c = self.__db.cursor()
            self.logger.info(f"Connected to '{self.path}'.")

            self.__check_tables()

            return

    def __check_tables(self) -> None:
        from .Tables import (TableGuilds, TableGuildBlacklist, TablePlayers, TableUsers, TableClans)

        Tables = [TableGuilds, TableGuildBlacklist, TablePlayers, TableUsers, TableClans]

        for Table in Tables:
            self.__c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                             (Table.name,))
            result = self.__c.fetchall()

            if not result:
                Table.create_table(self)

        return

    def close(self):
        self.__db.commit()
        self.__db.close()
        self.logger.info(f"Closed '{self.path}'.")

    def save_changes(self):
        self.__db.commit()
        self.logger.info(f"Saved '{self.path}'")

    @property
    def connection(self):
        return self.__db

    @property
    def cursor(self):
        return self.__c
