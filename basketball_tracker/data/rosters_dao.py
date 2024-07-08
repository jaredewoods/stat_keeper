# rosters_dao.py

import sqlite3

class RostersDAO:
    def __init__(self, db_path='data/rosters.sqlite'):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def fetch_roster_sans_headers(self):
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM RMHS_roster")
            return cursor.fetchall()

    def fetch_all_roster(self):
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM RMHS_roster")
            data = cursor.fetchall()
            headers = [description[0] for description in cursor.description]
            return headers, data

    def update_roster(self, jersey_no, last_name, first_name):
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE RMHS_roster SET LastName=?, FirstName=? WHERE JerseyNo=?",
                (last_name, first_name, jersey_no)
            )
            connection.commit()
