from Database.Data_base import DataBase


class Admin:
    db = None
    cursor = None
    connection = None

    def __init__(self, database: DataBase):
        self.cursor = database.get_cursor()
        self.connection = database.get_connection()
        self.db = database

    def drop_table(self):
        self.db.save_changes()

    def create_table_guilds(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS guilds ("
            "guild_id INTEGER PRIMARY KEY, "
            "guild_name TEXT NOT NULL, "
            "guild_owner INTEGER, "
            "clan_tag, "
            "clan_name,"
            "feed_channel, "
            "warlog_channel, "
            "clantable_channel, "
            "time_zone"
            ");"
        )
        self.db.save_changes()

    def create_table_messages(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS messages ("
            "message_id INTEGER PRIMARY KEY, "
            "message_type, "
            "type_value, "
            "message_time_stamp, "
            "tag TEXT"
            ");"
        )
        self.db.save_changes()

    def create_table_users(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS users ("
            "id INTEGER PRIMARY KEY, "
            "user_id INTEGER, "
            "player_tag TEXT,"
            "player_name TEXT"
            ");"
        )
        self.db.save_changes()

    def create_table_clans(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS clans ("
            "id PRIMARY KEY, "
            "tag TEXT, "
            "name TEXT, "
            "type TEXT, "
            "location_name TEXT, "
            "clan_level INTEGER, "
            "clan_points INTEGER, "
            "clan_versus_points INTEGER, "
            "required_trophies INTEGER, "
            "war_frequency TEXT, "
            "war_win_streak INTEGER, "
            "war_wins INTEGER, "
            "war_ties INTEGER, "
            "war_losses INTEGER, "
            "war_league_name TEXT, "
            "members INTEGER, "
            "label1_name TEXT, "
            "label2_name TEXT, "
            "label3_name TEXT, "
            "required_versus_trophies INTEGER, "
            "required_townhall_level INTEGER, "
            "chat_language_name TEXT, "
            "clan_capital__capital_peak_hall INTEGER, "
            "clan_capital__barbarian_camp_hall INTEGER, "
            "clan_capital__wizard_valley_hall INTEGER, "
            "clan_capital__balloon_lagoon_hall INTEGER, "
            "clan_capital__builders_workshop_hall INTEGER, "
            "clan_capital__dragon_cliffs_hall INTEGER, "
            "clan_capital__golem_quarry_hall INTEGER"
            ");"
        )
        self.db.save_changes()
        return

    def create_table_players(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS players ("
            "id PRIMARY KEY, "
            "tag TEXT, "
            "town_hall_level INTEGER, "
            "exp_level INTEGER, "
            "trophies INTEGER, "
            "best_trophies INTEGER, "
            "war_stars INTEGER, "
            "attack_wins INTEGER, "
            "defense_wins INTEGER, "
            "builder_hall_level INTEGER, "
            "versus_trophies INTEGER, "
            "best_versus_trophies, "
            "versus_battle_wins INTEGER, "
            "role TEXT, "
            "war_preference TEXT, "
            "donations INTEGER, "
            "donations_received INTEGER, "
            "clan_capital_contribution INTEGER, "
            "legend_trophies INTEGER, "
            "total_gold_looted INTEGER, "
            "total_elexir_looted INTEGER, "
            "total_town_halls_destroyed INTEGER, "
            "total_multiplayer_battles_won INTEGER, "
            "total_defenses_won INTEGER, "
            "total_capacity_donated INTEGER, "
            "total_dark_elexir_looted INTEGER, "
            "total_gold_cw_bonus_collected INTEGER, "
            "total_spell_capacity_donated INTEGER, "
            "builder_halls_destroyed INTEGER, "
            "total_clan_games_points INTEGER, "
            "total_clan_war_league_stars INTEGER, "
            "total_season_challenge_points INTEGER, "
            "total_times_super_troops_boosted INTEGER, "
            "total_siege_machines_donated INTEGER, "
            "total_capital_gold_looted INTEGER, "
            "total_capital_gold_contributed INTEGER,"
            "versus_battle_win_count INTEGER, "
            "timestamp"
            ");"
        )
        self.db.save_changes()
        return

    def alter_messages_add_tag(self):
        self.cursor.execute("ALTER TABLE messages ADD tag TEXT;")
        self.db.save_changes()
        print("success")
        return


if __name__ == "__main__":
    admin = Admin(DataBase())

    admin.drop_table("guilds")
    admin.create_table_players()
    admin.create_table_messages()
    admin.create_table_clans()
    admin.create_table_users()
    admin.create_table_guilds()

    admin.db.save_changes()
    admin.db.close()
