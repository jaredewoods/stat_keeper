import sqlite3
from PyQt6.QtCore import Qt, pyqtSlot


# noinspection SqlWithoutWhere
class PlayerStatsDAO:
    def __init__(self, db_path='data/player_stats.sqlite'):
        self.db_path = db_path
        self.connection = self.connect()

    # Connection Methods
    def connect(self):
        return sqlite3.connect(self.db_path)

    def close_db_connection(self):
        if self.connection:
            self.connection.close()

    # Raw Stats Methods
    def fetch_raw_stats(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM raw_stats")
        data = cursor.fetchall()
        headers = [description[0] for description in cursor.description]
        return headers, data

    def fetch_raw_stats_sans_headers(self, jersey_no):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM raw_stats WHERE JerseyNo=?", (jersey_no,))
        return cursor.fetchall()

    def update_raw_stats(self, data):
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

        cursor = self.connection.cursor()
        cursor.execute(
            """INSERT INTO raw_stats 
               (Date, Time, Venue, Opponent, Context, VideoTime, JerseyNo, LastName, FirstName, Code)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (date, time, venue, opponent, context, video_time, jersey_no, last_name, first_name, event)
        )
        self.connection.commit()
        print(f"Player stats updated for: {first_name} {last_name}")

    # Utility Methods
    def delete_last_added_row(self):
        cursor = self.connection.cursor()
        cursor.execute(
            """DELETE FROM raw_stats
               WHERE rowid = (SELECT rowid FROM raw_stats ORDER BY rowid DESC LIMIT 1)"""
        )
        self.connection.commit()
        print("Last added row deleted.")

    def clear_all_tables(self):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM raw_stats")
        cursor.execute("DELETE FROM processed_stats")
        self.connection.commit()
        print("All data cleared from raw_stats and processed_stats tables.")

    # Roster Methods
    def fetch_roster_sans_headers(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM roster")
        return cursor.fetchall()

    def fetch_roster(self):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM roster")
        data = cursor.fetchall()
        headers = [description[0] for description in cursor.description]
        return headers, data

    def update_roster(self, jersey_no, last_name, first_name):
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE roster SET LastName=?, FirstName=? WHERE JerseyNo=?",
            (last_name, first_name, jersey_no)
        )
        self.connection.commit()

    # Event Methods
    def fetch_events_sans_headers(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT Code, Description FROM basketball_events")
        return cursor.fetchall()

    def fetch_events(self):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM basketball_events")
        data = cursor.fetchall()
        headers = [description[0] for description in cursor.description]
        return headers, data

    def fetch_event_descriptions(self):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT Description FROM basketball_events")
        data = cursor.fetchall()
        descriptions = [row[0] for row in data]
        return descriptions
