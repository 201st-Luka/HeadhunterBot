from Database.Tables.table_clans import TableClans
from Database.Tables.table_guild import TableGuilds
from Database.Tables.table_messages import TableMessages
from Database.Tables.table_users import TableUsers
from Database.data_base import DataBase


class User:
    users: TableUsers
    guilds: TableGuilds
    clans: TableClans
    messages: TableMessages

    def __init__(self, database: DataBase):
        self.users, self.guilds, self.clans, self.messages = TableUsers(database), TableGuilds(database), TableClans(
            database), TableMessages(database)
