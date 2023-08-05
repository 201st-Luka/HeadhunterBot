from Database.Tables.table_clans import TableClans
from Database.Tables.table_guild import TableGuilds
from Database.Tables.table_guild_blacklist import TableGuildBlacklist
from Database.Tables.table_users import TableUsers


class User:
    __slots__ = ["users", "guilds", "clans", "guild_blacklist"]

    def __init__(self):
        self.users, self.guilds, self.clans, self.guild_blacklist = (TableUsers(), TableGuilds(), TableClans(),
                                                                     TableGuildBlacklist())
