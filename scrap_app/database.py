import sqlite3

class DatabaseHandler:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def fetch_races(self):
        self.cursor.execute('SELECT * FROM races')
        column_names = [desc[0] for desc in self.cursor.description]
        race_data = [dict(zip(column_names, row)) for row in self.cursor.fetchall()]
        return race_data

    def close(self):
        self.conn.close()

    def format_race(self, race):
        race_data = ""
        for value in race:
            race_data += f"Value: {value}\n"
        return race_data
    