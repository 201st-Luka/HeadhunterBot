from Bot.Database.Tables.table_clans import TableClans
from Bot.Database.Tables.table_guild import TableGuilds
from Bot.Database.Tables.table_guild_blacklist import TableGuildBlacklist
from Bot.Database.Tables.table_users import TableUsers


class User:
    __slots__ = ["users", "guilds", "clans", "guild_blacklist"]

    def __init__(self):
        self.users, self.guilds, self.clans, self.guild_blacklist = (TableUsers(), TableGuilds(), TableClans(),
                                                                     TableGuildBlacklist())
