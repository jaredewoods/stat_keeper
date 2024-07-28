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

    def update_player_stats(self, data):
        date = data['date']
        time = data['time']
        venue = data['venue']
        opponent = data['opponent']
        context = data['context']
        video_time = data['timecode']
        event = data['event']
        player_info = data['player'].strip().split()
        jersey_no = player_info[0]
        last_name = player_info[1]
        first_name = " ".join(player_info[2:])

        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """INSERT INTO player_stats (Date, Time, Venue, Opponent, Context, VideoTime, JerseyNo, LastName, FirstName, Code)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (date, time, venue, opponent, context, video_time, jersey_no, last_name, first_name, event)
            )
            connection.commit()
        print("Player stats inserted for:", first_name, last_name)  # Debug message

    def delete_last_added_row(self):
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """DELETE FROM player_stats
                   WHERE rowid = (SELECT rowid FROM player_stats ORDER BY rowid DESC LIMIT 1)"""
            )
            connection.commit()
        print("Last added row deleted.")  # Debug message
