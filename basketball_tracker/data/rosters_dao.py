# rosters_dao.py

import sqlite3

class RostersDAO:
    def __init__(self, db_path='data/rosters.sqlite'):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def get_all_roster_data(self):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM basketball_events")
        data = cursor.fetchall()
        connection.close()
        return data

    def update_roster(self, player_id, new_data):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute("UPDATE basketball_events SET data=? WHERE id=?", (new_data, player_id))
        connection.commit()
        connection.close()
