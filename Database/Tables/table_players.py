from Database.Database import DataBase, DataBaseLogger


class TablePlayers:
    table = "players"
    db = None
    cursor = None
    connection = None

    def __init__(self, database: DataBase):
        self.cursor = database.get_cursor()
        self.connection = database.get_connection()
        self.db = database

    @DataBaseLogger
    def insert_player_as_json(self, player_json: dict, timestamp: int):
        properties = ["tag", "townHallLevel", "expLevel", "trophies", "bestTrophies", "warStars", "attackWins",
                      "defenseWins", "builderHallLevel", "versusTrophies", "bestVersusTrophies", "versusBattleWins", "role",
                      "warPreference", "donations", "donationsReceived", "clanCapitalContributions", "legendTrophies"]

        values = [player_json.get(property, 0) if property != "legend_trophies" else player_json.get(property, {}).get(
            "value", 0) for property in properties]

        achievements = [player_json['achievements'][i]['completionInfo'].split(" ")[-1] for i in
                        [5, 6, 10, 12, 13, 14, 16, 21, 23, 27, 31, 33, 35, 39, 40, 41, 42, 28, timestamp]]
        placeholders = ", ".join("?" for _ in properties)

        query = f"INSERT INTO {self.table} ({', '.join(properties)}, timestamp) VALUES ({placeholders}, ?)"
        values.append(timestamp)

        self.cursor.execute(query, tuple(values + achievements))

        self.cursor.save_changes()
