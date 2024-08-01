# player_stats.py

import sqlite3
import os
from PyQt6.QtCore import Qt, pyqtSlot

class PlayerStatsDAO:
    def __init__(self, db_path='data/player_stats.sqlite'):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def fetch_all_player_stats(self):
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM player_stats")
            data = cursor.fetchall()
            headers = [description[0] for description in cursor.description]
            return headers, data

    def fetch_player_stats_sans_headers(self, jersey_no):
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM player_stats WHERE JerseyNo=?", (jersey_no,))
            return cursor.fetchall()

    # TODO: why won't '@pyqtSlot()' work here?
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
                """INSERT INTO player_stats 
                   (Date, Time, Venue, Opponent, Context, VideoTime, JerseyNo, LastName, FirstName, Code)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (date, time, venue, opponent, context, video_time, jersey_no, last_name, first_name, event)
            )
            connection.commit()

            # Fetch the updated event data for this player
            updated_data = self.fetch_player_stats_sans_headers(jersey_no)

            # Convert the fetched data to a DataFrame if needed
            events_df = pd.DataFrame(updated_data,
                                     columns=['Date', 'Time', 'Venue', 'Opponent', 'Context', 'VideoTime', 'JerseyNo',
                                              'LastName', 'FirstName', 'Code'])

            # Calculate aggregate statistics
            stats_logic = StatisticsLogic(events_df)
            updated_stats = stats_logic.aggregate_statistics()

            # Use the aggregated stats as needed
            self.update_sortable_statistics(cursor, updated_stats)
            connection.commit()

            # Refresh the stats tab to reflect the new statistics
            self.refresh_stats_tab()

        print(f"Player stats updated for: {first_name} {last_name}")

    def update_sortable_statistics(self, cursor, updated_stats):
        query = """INSERT OR REPLACE INTO sortable_statistics (PTS, FGM, FGA, "FG%", 3PM, 3PA, "3P%", FTM, FTA, "FT%", 
                       OREB, DREB, REB, AST, TOV, STL, BLK, PFL, SFL, IMP, GP)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        cursor.execute(query, (
            updated_stats['PTS'],
            updated_stats['FGM'],
            updated_stats['FGA'],
            updated_stats['FG%'],
            updated_stats['3PM'],
            updated_stats['3PA'],
            updated_stats['3P%'],
            updated_stats['FTM'],
            updated_stats['FTA'],
            updated_stats['FT%'],
            updated_stats['OREB'],
            updated_stats['DREB'],
            updated_stats['REB'],
            updated_stats['AST'],
            updated_stats['TOV'],
            updated_stats['STL'],
            updated_stats['BLK'],
            updated_stats['PFL'],
            updated_stats['SFL'],
            updated_stats.get('IMP', 0),  # Example calculation for IMP
            updated_stats['GP']
        ))

    def delete_last_added_row(self):
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """DELETE FROM player_stats
                   WHERE rowid = (SELECT rowid FROM player_stats ORDER BY rowid DESC LIMIT 1)"""
            )
            connection.commit()
        print("Last added row deleted.")
