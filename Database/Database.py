from logging import Logger
import sqlite3
from os import path
from typing import Callable

from pyclasher import MISSING


class DataBaseLogger:
    logger: Logger = MISSING

    def __call__(self, function: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            DataBaseLogger.logger.info(f"Database: {function.__name__} in {str(args[0].table).lower()}.")
            return function(*args, **kwargs)

        return wrapper


class DataBase:
    __db = None
    __c = None
    __instance = None

    def __new__(cls, db_path: str = None, db_name: str = None, logger: Logger = None) -> "DataBase":
        if db_path is None and db_name is None and logger is None and cls.__instance is None:
            raise AttributeError("db_path, db_name and logger must be different from None for the first initialisation.")
        if DataBase.__instance is None:
            DataBase.__instance = super().__new__(cls)

        return DataBase.__instance

    @property
    def instance(self):
        return DataBase.__instance

    def __init__(self, db_path: str = None, db_name: str = None, logger: Logger = None) -> None:
        if db_path is not None and db_name is not None and logger is not None:
            self.logger = logger.getChild("Db")
            DataBaseLogger.logger = self.logger
            self.path = path.join(db_path, db_name)
            self.__db = sqlite3.connect(self.path)
            self.__c = self.__db.cursor()
            self.logger.info(f"Connected to '{self.path}'.")
            return

    def close(self):
        self.__db.commit()
        self.__db.close()
        self.logger.info(f"Closed '{self.path}'.")

    def save_changes(self):
        self.__db.commit()
        self.logger.info(f"Saved '{self.path}'")

    def get_connection(self):
        return self.__db

    def get_cursor(self):
        return self.__c
