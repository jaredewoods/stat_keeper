# player_stats.py

import sqlite3


class PlayerStatsDAO:
    def __init__(self, db_path='data/player_stats.sqlite'):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def get_player_stats(self, player_id):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM player_stats WHERE player_id=?", (player_id,))
        data = cursor.fetchall()
        connection.close()
        return data

    def update_player_stats(self, player_id, new_data):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute("UPDATE player_stats SET data=? WHERE player_id=?", (new_data, player_id))
        connection.commit()
        connection.close()

