# events_dao.py

import sqlite3

class EventsDAO:
    def __init__(self, db_path='data/events.sqlite'):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def get_all_events(self):
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM basketball_events")
            return cursor.fetchall()

    def update_event(self, code, description):
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE basketball_events SET Description=? WHERE Code=?",
                (description, code)
            )
            connection.commit()
