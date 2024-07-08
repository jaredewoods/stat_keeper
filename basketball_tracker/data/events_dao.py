# events_dao.py

import sqlite3

class EventsDAO:
    def __init__(self, db_path='data/events.sqlite'):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def fetch_events_sans_headers(self):
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM basketball_events")
            return cursor.fetchall()

    def fetch_all_events(self):
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM basketball_events")
            data = cursor.fetchall()
            headers = [description[0] for description in cursor.description]
            return headers, data

    def update_event(self, code, description):
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE basketball_events SET Description=? WHERE Code=?",
                (description, code)
            )
            connection.commit()
