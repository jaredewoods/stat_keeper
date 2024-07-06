# events_dao.py

import sqlite3

class EventsDAO:
    def __init__(self, db_path='data/events.sqlite'):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def get_all_events(self):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM events")
        data = cursor.fetchall()
        connection.close()
        return data

    def update_event(self, event_id, new_data):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute("UPDATE events SET data=? WHERE id=?", (new_data, event_id))
        connection.commit()
        connection.close()
