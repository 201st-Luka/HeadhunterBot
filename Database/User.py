from Database.Tables.Guilds import Guilds
from Database.Tables.Users import Users
from Database.Tables.Clans import Clans
from Database.Tables.Messages import Messages
from Database.Data_base import DataBase


class User:
    users: Users
    guilds: Guilds
    clans: Clans
    messages: Messages

    def __init__(self, database: DataBase):
        self.users, self.guilds, self.clans, self.messages = Users(database), Guilds(database), Clans(database), Messages(database)


if __name__ == '__main__':
    def for_each_print(iterable: list | tuple):
        [print(line) for line in iterable]
    db = DataBase()
    user = User(db)
    # user.guilds.update_clan_tag_and_name(893218147740565524, "29ULYJ8LR", "Andor")
    print(user.guilds.fetch_clanname_and_tag(893218147740565524))
    db.close()
