import os

discordApiToken = "your api token"
clashOfClansHeaders = {
    "Accept": "application/json",
    "authorization": "Bearer your coc header"
}
messageOnGuildJoin = "Hello there!"
discordServer = "no discord server yet"
log = "HeadhunterBot.log"
current_working_directory = os.getcwd()
path = current_working_directory[:current_working_directory.find("HeadhunterBot") + 13]
database = "/".join((path, "Database", "HeadhunterBot.db"))
wars_per_page = 10
embed_color = 0x513B54
