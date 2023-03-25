from Database.Data_base import DataBase


class Admin:
    def __init__(self, db: DataBase):
        self.cursor = db.get_cursor()
        self.db = db

    @staticmethod
    def access_query(table_name: str) -> str:
        with open(f'Database/Queries/{table_name}.txt') as query_file:
            return query_file.read()

    def execute_query(self, query: str) -> None:
        self.cursor.execute(query)
        self.db.save_changes()

    def create_table_from_file(self, table_name: str) -> None:
        query = self.access_query(table_name)
        self.execute_query(query)

    def create_multiple_tables(self) -> None:
        table_names = ['table_clans', 'table_guilds', 'table_messages', 'table_users', 'table_players']
        for table_name in table_names:
            self.create_table_from_file(table_name)

    def close(self) -> None:
        self.db.save_changes()
        self.db.close()


if __name__ == "__main__":
    admin = Admin(DataBase())
    admin.create_multiple_tables()
    admin.close()
