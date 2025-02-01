# model/data_manager.py
import sqlite3
import time
import pandas as pd

# model/data_manager.py
import sqlite3
import threading
import pandas as pd

class DataManager:
    def __init__(self):
        # Store the database file path
        self.db_file = 'screentime.db'
        self._init_db()

    def _init_db(self):
        """Initialize the database tables."""
        with self._get_connection() as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS sessions
                (id INTEGER PRIMARY KEY, app TEXT, start REAL, end REAL)''')
            conn.execute('''CREATE TABLE IF NOT EXISTS app_switches
                (id INTEGER PRIMARY KEY, from_app TEXT, switch_count INTEGER)''')
            conn.commit()

    def _get_connection(self):
        """Create a new SQLite connection for the current thread."""
        return sqlite3.connect(self.db_file, check_same_thread=False)

    def log_app_switch(self, from_app, to_app, timestamp):
        """Log an app switch and update the switch count."""
        with self._get_connection() as conn:
            if from_app:
                # Update the end time of the previous app session
                conn.execute('''UPDATE sessions SET end = ?
                    WHERE id = (SELECT MAX(id) FROM sessions WHERE app = ?)''',
                    (timestamp, from_app))
                
                # Update the switch count for the from_app
                conn.execute('''INSERT OR IGNORE INTO app_switches (from_app, switch_count)
                    VALUES (?, 0)''', (from_app,))
                conn.execute('''UPDATE app_switches
                    SET switch_count = switch_count + 1
                    WHERE from_app = ?''', (from_app,))
            
            # Log the new app session
            conn.execute('INSERT INTO sessions (app, start, end) VALUES (?,?,?)',
                (to_app, timestamp, timestamp))
            
            conn.commit()

    def get_merged_sessions(self):
        """Get the total time spent on each app and the number of switches from each app."""
        with self._get_connection() as conn:
            # Get session data
            df = pd.read_sql('SELECT * FROM sessions', conn)
            df['duration'] = df['end'] - df['start']
            merged = df.groupby('app').agg({'duration': 'sum'}).reset_index()
            
            # Get switch counts
            switch_counts = pd.read_sql('SELECT from_app, switch_count FROM app_switches', conn)
            switch_counts.rename(columns={'from_app': 'app'}, inplace=True)
            
            # Merge session data with switch counts
            merged = pd.merge(merged, switch_counts, on='app', how='left')
            merged['switch_count'] = merged['switch_count'].fillna(0).astype(int)
            
            return merged.to_dict('records')

    def get_switch_counts(self):
        """Get the number of times the user switched from each app."""
        with self._get_connection() as conn:
            df = pd.read_sql('SELECT from_app, switch_count FROM app_switches', conn)
            return df.to_dict('records')
        
def test_data_manager():
    # Initialize the data manager
    data_manager = DataManager()

    # Simulate app switches
    data_manager.log_app_switch(None, "chrome", time.time())
    time.sleep(1)
    data_manager.log_app_switch("chrome", "code", time.time())
    time.sleep(1)
    data_manager.log_app_switch("code", "chrome", time.time())
    time.sleep(1)
    data_manager.log_app_switch("chrome", "code", time.time())

    # Get merged sessions and switch counts
    sessions = data_manager.get_merged_sessions()
    switch_counts = data_manager.get_switch_counts()

    # Print results
    print("Merged Sessions:")
    for session in sessions:
        print(session)

    print("\nSwitch Counts:")
    for switch in switch_counts:
        print(switch)

if __name__ == "__main__":
    test_data_manager()