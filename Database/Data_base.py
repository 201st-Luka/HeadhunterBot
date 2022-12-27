import logging
import sqlite3
from Bot.Variables import database


class DataBase:
    __db = None
    __c = None
    __dbName = database

    def __init__(self):
        self.__db = sqlite3.connect(self.__dbName)
        self.__c = self.__db.cursor()
        logging.info(f"{self.__dbName}\tConnected!")

    def close(self):
        self.__db.commit()
        self.__db.close()
        logging.info(f"{self.__dbName}\tClosed!")

    def save_changes(self):
        self.__db.commit()
        logging.info(f"{self.__dbName}\tSaved!")

    def get_connection(self):
        return self.__db

    def get_cursor(self):
        return self.__c
