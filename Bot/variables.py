import os


class Variables:
    def __init__(self):
        self.discord_api_token = "<YOUR API TOKEN>"
        self.clash_of_clans_headers = {
            "Accept": "application/json",
            "authorization": "Bearer <YOUR COC KEY>"
        }
        self.message_on_guild_join = "Hello there!"
        self.discord_server = "no discord server yet"
        self.log_file_name = "HeadhunterBot.log"
        self.current_working_directory = os.getcwd()
        self.headhunter_bot_directory_path = self.current_working_directory[
                                             :self.current_working_directory.find("HeadhunterBot") + 13]
        self.database_file_path = "\\".join((self.headhunter_bot_directory_path, "Database", "HeadhunterBot.db"))
        self.wars_per_page = 10
        self.embed_color = 0x513B54
