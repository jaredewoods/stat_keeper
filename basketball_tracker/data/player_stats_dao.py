# player_stats_dao.py

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
            cursor.execute("SELECT * FROM raw_stats")
            data = cursor.fetchall()
            headers = [description[0] for description in cursor.description]
            return headers, data

    def fetch_player_stats_sans_headers(self, jersey_no):
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM raw_stats WHERE JerseyNo=?", (jersey_no,))
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
                """INSERT INTO raw_stats 
                   (Date, Time, Venue, Opponent, Context, VideoTime, JerseyNo, LastName, FirstName, Code)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (date, time, venue, opponent, context, video_time, jersey_no, last_name, first_name, event)
            )
            connection.commit()
        self.aggregate_and_update_stats()
        print(f"Player stats updated for: {first_name} {last_name}")

    @staticmethod
    def update_processed_stats(cursor, updated_stats):
        query = r"""
        INSERT OR REPLACE INTO "processed_stats" 
        (JerseyNo, FirstName, LastName, PTS, FGM, FGA, "FG%", "3PM", "3PA", "3P%", FTM, FTA, "FT%", OREB, DREB, REB, AST, TOV, STL, BLK, PFL, SFL) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (
            updated_stats['JerseyNo'],
            updated_stats['FirstName'],
            updated_stats['LastName'],
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
            updated_stats['SFL']
        ))

    def delete_last_added_row(self):
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """DELETE FROM raw_stats
                   WHERE rowid = (SELECT rowid FROM raw_stats ORDER BY rowid DESC LIMIT 1)"""
            )
            connection.commit()
        print("Last added row deleted.")

    def aggregate_and_update_stats(self):
        last_processed_id = self.get_last_processed_record()

        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM raw_stats WHERE rowid > ?", (last_processed_id,))
            new_data = cursor.fetchall()
            headers = [description[0] for description in cursor.description]

        aggregated_stats = {}

        for event in new_data:
            jersey_no = event[headers.index('JerseyNo')]
            first_name = event[headers.index('FirstName')]
            last_name = event[headers.index('LastName')]
            player_key = (jersey_no, first_name, last_name)

            if player_key not in aggregated_stats:
                aggregated_stats[player_key] = {
                    'JerseyNo': jersey_no,
                    'FirstName': first_name,
                    'LastName': last_name,
                    'PTS': 0, 'FGM': 0, 'FGA': 0, '3PM': 0, '3PA': 0,
                    'FTM': 0, 'FTA': 0, 'OREB': 0, 'DREB': 0, 'REB': 0,
                    'AST': 0, 'TOV': 0, 'STL': 0, 'BLK': 0, 'PFL': 0,
                    'SFL': 0,
                }

            event_code = event[headers.index('Code')]
            if event_code == '2pt Field Goal':
                aggregated_stats[player_key]['PTS'] += 2
                aggregated_stats[player_key]['FGM'] += 1
                aggregated_stats[player_key]['FGA'] += 1
            elif event_code == 'Missed 2pt':
                aggregated_stats[player_key]['FGA'] += 1
            elif event_code == '3pt Field Goal':
                aggregated_stats[player_key]['PTS'] += 3
                aggregated_stats[player_key]['3PM'] += 1
                aggregated_stats[player_key]['3PA'] += 1
            elif event_code == 'Missed 3pt':
                aggregated_stats[player_key]['3PA'] += 1
            elif event_code == 'Free Throw':
                aggregated_stats[player_key]['PTS'] += 1
                aggregated_stats[player_key]['FTM'] += 1
                aggregated_stats[player_key]['FTA'] += 1
            elif event_code == 'Missed Free Throw':
                aggregated_stats[player_key]['FTA'] += 1
            elif event_code == 'Off. Rebound':
                aggregated_stats[player_key]['OREB'] += 1
                aggregated_stats[player_key]['REB'] += 1
            elif event_code == 'Def. Rebound':
                aggregated_stats[player_key]['DREB'] += 1
                aggregated_stats[player_key]['REB'] += 1
            elif event_code == 'Assist':
                aggregated_stats[player_key]['AST'] += 1
            elif event_code == 'Turnover':
                aggregated_stats[player_key]['TOV'] += 1
            elif event_code == 'Steal':
                aggregated_stats[player_key]['STL'] += 1
            elif event_code == 'Block':
                aggregated_stats[player_key]['BLK'] += 1
            elif event_code == 'Personal Foul':
                aggregated_stats[player_key]['PFL'] += 1
            elif event_code == 'Shooting Foul':
                aggregated_stats[player_key]['SFL'] += 1

        with self.connect() as connection:
            cursor = connection.cursor()
            for player_key, stats in aggregated_stats.items():
                stats['FG%'] = stats['FGM'] / stats['FGA'] if stats['FGA'] > 0 else 0
                stats['3P%'] = stats['3PM'] / stats['3PA'] if stats['3PA'] > 0 else 0
                stats['FT%'] = stats['FTM'] / stats['FTA'] if stats['FTA'] > 0 else 0
                self.update_processed_stats(cursor, stats)
            connection.commit()

    def fetch_all_processed_stats(self):
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM processed_stats")
            data = cursor.fetchall()
            headers = [description[0] for description in cursor.description]
            return headers, data

    def clear_all_tables(self):
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM raw_stats")
            cursor.execute("DELETE FROM processed_stats")
            connection.commit()
        print("All data cleared from raw_stats and processed_stats tables.")

    def get_last_processed_record(self):
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT MAX(rowid) FROM processed_stats")
            result = cursor.fetchone()
            return result[0] if result else 0
