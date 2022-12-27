from Bot.Methods import get_achievement_completion_info as gaci
from Database.Data_base import DataBase


class Players:
    table = "players"
    db = None
    cursor = None
    connection = None

    def __init__(self, database: DataBase):
        self.cursor = database.get_cursor()
        self.connection = database.get_connection()
        self.db = database
        return

    def insert_player_as_json(self, player_json, timestamp):
        self.cursor.execute("INSERT INTO players("
                            "tag, "
                            "town_hall_level, "
                            "exp_level, "
                            "trophies, "
                            "best_trophies, "
                            "war_stars, "
                            "attack_wins, "
                            "defense_wins, "
                            "builder_hall_level, "
                            "versus_trophies, "
                            "best_versus_trophies, "
                            "versus_battle_wins, "
                            "role, "
                            "war_preference, "
                            "donations, "
                            "donations_received, "
                            "clan_capital_contribution, "
                            "legend_trophies, "
                            "total_gold_looted, "
                            "total_elexir_looted, "
                            "total_town_halls_destroyed, "
                            "total_multiplayer_battles_won, "
                            "total_defenses_won, "
                            "total_capacity_donated, "
                            "total_dark_elexir_looted, "
                            "total_gold_cw_bonus_collected, "
                            "total_spell_capacity_donated, "
                            "builder_halls_destroyed, "
                            "total_clan_games_points, "
                            "total_clan_war_league_stars, "
                            "total_season_challenge_points, "
                            "total_times_super_troops_boosted, "
                            "total_siege_machines_donated, "
                            "total_capital_gold_looted, "
                            "total_capital_gold_contributed,"
                            "versus_battle_win_count, "
                            "timestamp"
                            ") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
                            "?, ?, ?)",
                            (player_json['tag'], str(player_json['townHallLevel']), str(player_json['expLevel']), str(player_json['trophies']),
                             str(player_json['bestTrophies']), str(player_json['warStars']), str(player_json['attackWins']),
                             str(player_json['defenseWins']), str(player_json['builderHallLevel']), str(player_json['versusTrophies']),
                             str(player_json['bestVersusTrophies']), str(player_json['versusBattleWins']), player_json['role'],
                             player_json['warPreference'], str(player_json['donations']), str(player_json['donationsReceived']),
                             str(player_json['clanCapitalContribution']), str(player_json['legendTrophies']) if player_json['legendTrophies'] in player_json else "0",
                             gaci(player_json, 5), gaci(player_json, 6), gaci(player_json, 10), gaci(player_json, 12), gaci(player_json, 13),
                             gaci(player_json, 14), gaci(player_json, 16), gaci(player_json, 21), gaci(player_json, 23), gaci(player_json, 27),
                             gaci(player_json, 31), gaci(player_json, 33), gaci(player_json, 35), gaci(player_json, 39), gaci(player_json, 40),
                             gaci(player_json, 41), gaci(player_json, 42), gaci(player_json, 28), timestamp
                             )
                            )
        self.db.save_changes()
        return
