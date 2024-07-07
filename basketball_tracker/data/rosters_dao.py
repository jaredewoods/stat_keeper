# rosters_dao.py

import sqlite3

class RostersDAO:
    def __init__(self, db_path='data/rosters.sqlite'):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def fetch_all(self):
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM RMHS_roster")
            return cursor.fetchall()

    def update_roster(self, jersey_no, last_name, first_name):
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE RMHS_roster SET LastName=?, FirstName=? WHERE JerseyNo=?",
                (last_name, first_name, jersey_no)
            )
            connection.commit()
