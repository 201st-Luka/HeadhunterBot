from .abc import AbcTable


class TableClans(AbcTable):
    name = "clans"
    create_table_query = (
        "CREATE TABLE clans ("
        "id INTEGER PRIMARY KEY,"
        "clan TEXT"
        ");"
    )
