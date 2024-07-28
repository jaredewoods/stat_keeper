# player_stats.py

import sqlite3
import os

class PlayerStatsDAO:
    def __init__(self, db_path='data/player_stats.sqlite'):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def fetch_all_player_stats(self):
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM player_stats")
            data = cursor.fetchall()
            headers = [description[0] for description in cursor.description]
            return headers, data

    def fetch_player_stats_sans_headers(self, jersey_no):
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM player_stats WHERE JerseyNo=?", (jersey_no,))
            return cursor.fetchall()


