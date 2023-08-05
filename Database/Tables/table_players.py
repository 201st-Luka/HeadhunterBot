from Database import DataBase, DataBaseLogger


Table = "players"


def create_table(db: DataBase):
    db.cursor.execute(
        "CREATE TABLE players ("
        "tag TEXT,"
        "townHallLevel INTEGER,"
        "expLevel INTEGER,"
        "trophies INTEGER,"
        "bestTrophies INTEGER,"
        "warStars INTEGER,"
        "attackWins INTEGER,"
        "defenseWins INTEGER,"
        "builderHallLevel INTEGER,"
        "versusTrophies INTEGER,"
        "bestVersusTrophies INTEGER,"
        "versusBattleWins INTEGER,"
        "role TEXT,"
        "warPreference TEXT,"
        "donations INTEGER,"
        "donationsReceived INTEGER,"
        "clanCapitalContributions INTEGER,"
        "legendTrophies INTEGER"
        ");"
    )
    db.save_changes()

    DataBaseLogger.logger.info(f"Created table {Table}.")

    return


class TablePlayers:
    table = Table
    db = None
    cursor = None
    connection = None

    def __init__(self, database: DataBase):
        self.cursor = database.cursor
        self.connection = database.connection
        self.db = database

    @DataBaseLogger()
    def insert_player_as_json(self, player_json: dict, timestamp: int):
        properties = ["tag", "townHallLevel", "expLevel", "trophies", "bestTrophies", "warStars", "attackWins",
                      "defenseWins", "builderHallLevel", "versusTrophies", "bestVersusTrophies", "versusBattleWins", "role",
                      "warPreference", "donations", "donationsReceived", "clanCapitalContributions", "legendTrophies"]

        values = [player_json.get(property, 0) if property != "legend_trophies" else player_json.get(property, {}).get(
            "value", 0) for property in properties]

        achievements = [player_json['achievements'][i]['completionInfo'].split(" ")[-1] for i in
                        [5, 6, 10, 12, 13, 14, 16, 21, 23, 27, 31, 33, 35, 39, 40, 41, 42, 28, timestamp]]
        placeholders = ", ".join("?" for _ in properties)

        query = f"INSERT INTO {self.table} ({', '.join(properties)}, timestamp) VALUES ({placeholders}, ?);"
        values.append(timestamp)

        self.cursor.execute(query, tuple(values + achievements))

        self.cursor.save_changes()
