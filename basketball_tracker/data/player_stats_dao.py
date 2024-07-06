# player_stats.py

import sqlite3
import os

class PlayerStatsDAO:
    def __init__(self, db_path='data/player_stats.sqlite'):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def fetch_all(self, table_name):
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            data = cursor.fetchall()
            headers = [description[0] for description in cursor.description]
            return headers, data

    def get_player_stats(self, jersey_no):
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM player_stats WHERE JerseyNo=?", (jersey_no,))
            return cursor.fetchall()

    def update_player_stat(self, date, time, venue, opponent, context, video_time, jersey_no, last_name, first_name, code):
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """UPDATE player_stats SET Time=?, Venue=?, Opponent=?, Context=?, VideoTime=?, LastName=?, FirstName=?, Code=?
                   WHERE Date=? AND JerseyNo=?""",
                (time, venue, opponent, context, video_time, last_name, first_name, code, date, jersey_no)
            )
            connection.commit()
