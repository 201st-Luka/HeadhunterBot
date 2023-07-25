from Database.Tables.table_clans import TableClans
from Database.Tables.table_guild import TableGuilds
from Database.Tables.table_messages import TableMessages
from Database.Tables.table_users import TableUsers


class User:
    users: TableUsers
    guilds: TableGuilds
    clans: TableClans
    messages: TableMessages

    __slots__ = ["users", "guilds", "clans", "messages"]

    def __init__(self):
        self.users, self.guilds, self.clans, self.messages = TableUsers(), TableGuilds(), TableClans(), TableMessages()
