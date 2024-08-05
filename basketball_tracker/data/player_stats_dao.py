import sqlite3
from PyQt6.QtCore import Qt, pyqtSlot
from core.signal_distributor import SignalDistributor


# noinspection SqlWithoutWhere
class PlayerStatsDAO:
    def __init__(self, signal_distributor=None):
        self.db_path = 'data/player_stats.sqlite'
        self.sd = signal_distributor
        self.connection = self.connect()
        self.initialize_processed_stats()

    # Connection Methods
    def connect(self):
        return sqlite3.connect(self.db_path)

    def close_db_connection(self):
        if self.connection:
            self.connection.close()

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
        try:
            date = data['date']
            time = data['time']
            venue = data['venue']
            opponent = data['opponent']
            context = data['context']
            video_time = data['timecode']
            event = data['event']
            player_info = data['player'].strip().split()

            # Ensure that player_info contains at least 2 elements (jersey number and last name)
            if len(player_info) < 2:
                raise IndexError("Player information is incomplete. Expected at least Jersey Number and Last Name.")

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
            self.update_processed_stats_based_on_raw(data)

        except IndexError as e:
            print(f"Error: {e}. Data not inserted into raw_stats.")  # Debugging print
            # Optional: Emit a signal to notify the UI or log the error elsewhere

    # Processed Methods
    def initialize_processed_stats(self):
        cursor = self.connection.cursor()

        cursor.execute("DELETE FROM processed_stats")

        cursor.execute("""
            INSERT INTO processed_stats 
            ("JerseyNo", "FirstName", "LastName", "PTS", "FGM", "FGA", "FG%", "3PM", "3PA", "3P%", 
             "FTM", "FTA", "FT%", "OREB", "DREB", "REB", "AST", "TOV", "STL", "BLK", "PFL", "SFL")
            SELECT JerseyNo, FirstName, LastName, 0, 0, 0, 0.0, 0, 0, 0.0, 0, 0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            FROM roster
        """)

        self.connection.commit()
        print("3 Processed stats initialized with roster data.")

    def fetch_processed_stats(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM processed_stats")
        data = cursor.fetchall()
        headers = [description[0] for description in cursor.description]
        return headers, data

    def update_processed_stats_based_on_raw(self, data):
        # Extract relevant fields from the data
        jersey_no = data['player'].strip().split()[0]
        event = data['event']

        # Initialize the update query and values
        update_query_parts = []

        # Update stats based on the event type
        if event == '2pt Field Goal':
            update_query_parts.append('PTS = PTS + 2')
            update_query_parts.append('FGM = FGM + 1')
            update_query_parts.append('FGA = FGA + 1')
        elif event == '3pt Field Goal':
            update_query_parts.append('PTS = PTS + 3')
            update_query_parts.append('"3PM" = "3PM" + 1')
            update_query_parts.append('"3PA" = "3PA" + 1')
        elif event == 'Free Throw':
            update_query_parts.append('PTS = PTS + 1')
            update_query_parts.append('FTM = FTM + 1')
            update_query_parts.append('FTA = FTA + 1')
        elif event == 'Missed 2pt':
            update_query_parts.append('FGA = FGA + 1')
        elif event == 'Missed 3pt':
            update_query_parts.append('"3PA" = "3PA" + 1')
        elif event == 'Missed FT':
            update_query_parts.append('FTA = FTA + 1')
        elif event == 'Off. Rebound':
            update_query_parts.append('OREB = OREB + 1')
            update_query_parts.append('REB = REB + 1')
        elif event == 'Def. Rebound':
            update_query_parts.append('DREB = DREB + 1')
            update_query_parts.append('REB = REB + 1')
        elif event == 'Assist':
            update_query_parts.append('AST = AST + 1')
        elif event == 'Turnover':
            update_query_parts.append('TOV = TOV + 1')
        elif event == 'Steal':
            update_query_parts.append('STL = STL + 1')
        elif event == 'Block':
            update_query_parts.append('BLK = BLK + 1')
        elif event == 'Personal Foul':
            update_query_parts.append('PFL = PFL + 1')
        elif event == 'Shooting Foul':
            update_query_parts.append('SFL = SFL + 1')

        # Execute the first part of the update (statistical changes)
        if update_query_parts:
            update_query = "UPDATE processed_stats SET " + ", ".join(update_query_parts)
            update_query += " WHERE JerseyNo = ?"
            cursor = self.connection.cursor()
            cursor.execute(update_query, (jersey_no,))
            self.connection.commit()

        # Now calculate the percentages based on the updated stats
        percentage_update_query_parts = [
            '"FG%" = ROUND((CAST(FGM AS FLOAT) / CASE WHEN FGA = 0 THEN 1 ELSE FGA END) * 100, 1)',
            '"3P%" = ROUND((CAST("3PM" AS FLOAT) / CASE WHEN "3PA" = 0 THEN 1 ELSE "3PA" END) * 100, 1)',
            '"FT%" = ROUND((CAST(FTM AS FLOAT) / CASE WHEN FTA = 0 THEN 1 ELSE FTA END) * 100, 1)'
        ]

        percentage_update_query = "UPDATE processed_stats SET " + ", ".join(percentage_update_query_parts)
        percentage_update_query += " WHERE JerseyNo = ?"
        cursor.execute(percentage_update_query, (jersey_no,))
        self.connection.commit()

        # Emit the signal to refresh the UI
        self.sd.SIG_RawStatsProcessed.emit()
