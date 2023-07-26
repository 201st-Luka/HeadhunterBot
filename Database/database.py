from logging import Logger
import sqlite3
from os import path
from time import sleep
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
            DataBaseLogger.logger = self.logger
            self.path = db_path
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
