from importlib.util import spec_from_file_location, module_from_spec
from logging import Logger
from os import path, getcwd, listdir
from sqlite3 import connect
from typing import Callable, Any

from pyclasher import MISSING


class DataBaseLogger:
    logger: Logger = MISSING

    def __call__(self, function: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args, **kwargs) -> Any:
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
            self.__db = connect(self.path)
            self.__c = self.__db.cursor()
            self.logger.info(f"Connected to '{self.path}'.")

            self.__check_tables()

            return

    def __check_tables(self) -> None:
        cwd = getcwd()
        tables_path = path.join(cwd, "Database", "Tables")
        py_files = [module for module in listdir(tables_path) if module[-3:] == ".py"]

        query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        for file in py_files:
            file_path = path.join("Database", "Tables", file)

            spec = spec_from_file_location(file, file_path)
            module = module_from_spec(spec)
            spec.loader.exec_module(module)

            self.__c.execute(query, (module.Table,))
            result = self.__c.fetchall()

            if not result:
                module.create_table(self)

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
