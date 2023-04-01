import logging
import sqlite3

from Bot.variables import Variables


class DataBase:
    __db = None
    __c = None
    __vars = Variables()

    def __init__(self):
        self.__db = sqlite3.connect(self.__vars.database_file_path)
        self.__c = self.__db.cursor()
        logging.info(f"{self.__vars.database_file_path}\tConnected!")

    def close(self):
        self.__db.commit()
        self.__db.close()
        logging.info(f"{self.__vars.database_file_path}\tClosed!")

    def save_changes(self):
        self.__db.commit()
        logging.info(f"{self.__vars.database_file_path}\tSaved!")

    def get_connection(self):
        return self.__db

    def get_cursor(self):
        return self.__c
