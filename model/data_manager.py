# model/data_manager.py
import sqlite3
import pandas as pd

class DataManager:
    def __init__(self):
        self.conn = sqlite3.connect('screentime.db')
        self._init_db()

    def _init_db(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS sessions
            (id INTEGER PRIMARY KEY, app TEXT, start REAL, end REAL)''')
        self.conn.commit()

    def log_app_switch(self, from_app, to_app, timestamp):
        if from_app:
            self.conn.execute('''UPDATE sessions SET end = ?
                WHERE id = (SELECT MAX(id) FROM sessions WHERE app = ?)''',
                (timestamp, from_app))
        self.conn.execute('INSERT INTO sessions (app, start, end) VALUES (?,?,?)',
            (to_app, timestamp, timestamp))
        self.conn.commit()

    def get_merged_sessions(self):
        df = pd.read_sql('SELECT * FROM sessions', self.conn)
        df['duration'] = df['end'] - df['start']
        merged = df.groupby('app').agg({'duration': 'sum'}).reset_index()
        return merged.to_dict('records')