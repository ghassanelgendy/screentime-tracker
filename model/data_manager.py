# model/data_manager.py
import sqlite3
import threading
import pandas as pd
from datetime import datetime, timedelta

class DataManager:
    _lock = threading.Lock()
    
    def __init__(self):
        self.db_file = 'screentime.db'
        self._init_db()
        
    def _init_db(self):
        """Initialize database with proper schema"""
        with self._get_connection() as conn:
            # Enable foreign key support
            conn.execute("PRAGMA foreign_keys = ON")
            print("Creating application and category tables\n\n")
            # Application and Category tables
            conn.execute('''
                        CREATE TABLE IF NOT EXISTS application (
                        app_id INTEGER PRIMARY KEY,
                        app_name TEXT NOT NULL,
                        executable_path TEXT UNIQUE NOT NULL,
                        category_id INTEGER REFERENCES category(category_id)
            )''')
            
            conn.execute('''CREATE TABLE IF NOT EXISTS category (
                            category_id INTEGER PRIMARY KEY,
                            category_name TEXT UNIQUE NOT NULL,
                            daily_limit INTEGER
            )''')
            
            # Session tracking
            print("Creating session table\n\n")       
            conn.execute('''CREATE TABLE IF NOT EXISTS session (
                        session_id INTEGER PRIMARY KEY,
                        app_id INTEGER NOT NULL REFERENCES application(app_id),
                        start_time DATETIME NOT NULL,
                        end_time DATETIME DEFAULT NULL,  -- Allow NULL while session is active
                        duration INTEGER GENERATED ALWAYS AS (
                            CASE 
                                WHEN end_time IS NOT NULL 
                                        THEN CAST((strftime('%s', end_time) - strftime('%s', start_time)) AS INTEGER) 
                                ELSE NULL 
                            END
                        ) VIRTUAL
                )''')
            
            # App switch tracking
            print("Creating app switch table\n\n")
            conn.execute('''CREATE TABLE IF NOT EXISTS app_switch (
                switch_id INTEGER PRIMARY KEY,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                from_app_id INTEGER NOT NULL REFERENCES application(app_id),
                to_app_id INTEGER REFERENCES application(app_id)
            )''')
            
            # Idle time tracking
            print("Creating idle session table\n\n")
            conn.execute('''CREATE TABLE IF NOT EXISTS idle_session (
                    idle_id INTEGER PRIMARY KEY,
                    start_time DATETIME NOT NULL,
                    end_time DATETIME DEFAULT NULL,  -- Allow NULL while idle is active
                    duration INTEGER GENERATED ALWAYS AS (
                        CASE 
                            WHEN end_time IS NOT NULL 
                            THEN CAST((strftime('%s', end_time) - strftime('%s', start_time)) AS INTEGER) 
                            ELSE NULL 
                        END
                    ) VIRTUAL
                )''')
            
            # Daily aggregated stats
            conn.execute('''CREATE TABLE IF NOT EXISTS daily_stats (
                date DATE PRIMARY KEY,
                total_usage INTEGER NOT NULL,
                app_switch_count INTEGER NOT NULL,
                total_idle_time INTEGER NOT NULL
            )''')
            
            # Create indexes
            conn.execute('''CREATE INDEX IF NOT EXISTS idx_session_times 
                ON session(start_time, end_time)''')
            conn.execute('''CREATE INDEX IF NOT EXISTS idx_switch_times 
                ON app_switch(timestamp)''')
            conn.commit()

    def _get_connection(self):
        """Get thread-safe connection with connection pooling"""
        return sqlite3.connect(self.db_file, check_same_thread=False)
    def get_app(self, app_id):
        """Retrieve application details by app_id."""
        with self._lock, self._get_connection() as conn:
            cursor = conn.execute(
                'SELECT app_name, executable_path FROM application WHERE app_id = ?',
                (app_id,)
            )
            return cursor.fetchone()  # Returns (app_name, executable_path) or None

    def create_app(self, app_name, executable_path):
        """Create a new application entry and return its ID."""
        with self._lock, self._get_connection() as conn:
            conn.execute(
                'INSERT INTO application (app_name, executable_path) VALUES (?, ?)',
                (app_name, executable_path)
            )
            app_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
            conn.commit()
            return app_id

    def log_app_switch(self, from_app_id, to_app_id):
        """Log an application switch with proper session tracking"""
        with self._lock, self._get_connection() as conn:
            now = datetime.now().isoformat()
            
            # End previous session
            if from_app_id:
                conn.execute('''UPDATE session SET end_time = ?
                    WHERE session_id = (
                        SELECT session_id FROM session 
                        WHERE app_id = ? 
                        ORDER BY end_time DESC 
                        LIMIT 1
                    )''', (now, from_app_id))
                
            # Log the switch
            conn.execute('''INSERT INTO app_switch (from_app_id, to_app_id, timestamp)
                VALUES (?, ?, ?)''', (from_app_id, to_app_id, now))
            
            # Start new session
            conn.execute('''INSERT INTO session (app_id, start_time, end_time)
                VALUES (?, ?, ?)''', (to_app_id, now, now))
            
            conn.commit()

    def log_idle_time(self, start_time, end_time):
        """Log an idle period"""
        with self._lock, self._get_connection() as conn:
            conn.execute('''INSERT INTO idle_session (start_time, end_time)
                VALUES (?, ?)''', (start_time.isoformat(), end_time.isoformat()))
            conn.commit()

    def get_merged_sessions(self, timeframe='day'):
        """Get aggregated session data with switch counts"""
        time_filter = {
            'day': 'datetime("now", "-1 day")',
            'week': 'datetime("now", "-7 days")',
            'hour': 'datetime("now", "-1 hour")'
        }.get(timeframe, 'datetime("now", "-1 day")')

        query = f'''
            SELECT 
                a.app_name,
                SUM(s.duration) AS total_duration,
                COUNT(DISTINCT sw.switch_id) AS switch_count
            FROM session s
            JOIN application a ON s.app_id = a.app_id
            LEFT JOIN app_switch sw ON s.app_id = sw.to_app_id
                AND sw.timestamp >= {time_filter}
            WHERE s.start_time >= {time_filter}
            GROUP BY a.app_id
            ORDER BY total_duration DESC
        '''
        
        with self._get_connection() as conn:
            df = pd.read_sql(query, conn)
            print(df)
            return df.to_dict('records')

    def update_daily_stats(self):
        """Calculate and store daily aggregated stats"""
        with self._lock, self._get_connection() as conn:
            # Delete existing stats for today
            today = datetime.now().date().isoformat()
            conn.execute('DELETE FROM daily_stats WHERE date = ?', (today,))
            
            # Calculate new stats
            conn.execute(f'''
                INSERT INTO daily_stats (date, total_usage, app_switch_count, total_idle_time)
                SELECT
                    DATE('now'),
                    COALESCE(SUM(s.duration), 0),
                    COALESCE(COUNT(sw.switch_id), 0),
                    COALESCE(SUM(i.duration), 0)
                FROM session s
                LEFT JOIN app_switch sw ON DATE(sw.timestamp) = DATE('now')
                LEFT JOIN idle_session i ON DATE(i.start_time) = DATE('now')
                WHERE DATE(s.start_time) = DATE('now')
            ''')
            conn.commit()

    def get_time_based_data(self, period='day'):
        """Get data aggregated by time period"""
        time_formats = {
            'hour': '%Y-%m-%d %H:00',
            'day': '%Y-%m-%d',
            'week': '%Y-%W'
        }
        fmt = time_formats.get(period, '%Y-%m-%d')

        query = f'''
            SELECT 
                strftime('{fmt}', s.start_time) AS period,
                a.app_name,
                SUM(s.duration) AS total_duration,
                COUNT(sw.switch_id) AS switch_count
            FROM session s
            JOIN application a ON s.app_id = a.app_id
            LEFT JOIN app_switch sw ON sw.timestamp BETWEEN s.start_time AND s.end_time
            GROUP BY period, a.app_id
            ORDER BY period
        '''
        
        with self._get_connection() as conn:
            return pd.read_sql(query, conn).to_dict('records')

    # Additional helper methods
    def get_total_idle_time(self, timeframe='today'):
        """Get total idle time for specified timeframe"""
        filters = {
            'today': "DATE(start_time) = DATE('now')",
            'week': "start_time >= DATE('now', '-7 days')",
            'hour': "start_time >= DATETIME('now', '-1 hour')"
        }
        where_clause = filters.get(timeframe, filters['today'])
        
        with self._get_connection() as conn:
            cursor = conn.execute(f'''
                SELECT SUM(duration) FROM idle_session WHERE {where_clause}
            ''')
            return cursor.fetchone()[0] or 0

    def get_app_switch_count(self, app_id=None):
        """Get total or app-specific switch counts"""
        query = """SELECT COUNT(*) 
            FROM app_switch 
            WHERE from_app_id IS NOT NULL AND from_app_id != 0 
            AND to_app_id IS NOT NULL AND to_app_id != 0"""
        if app_id:
            query += f' WHERE from_app_id = {app_id}'
            
        with self._get_connection() as conn:
            cursor = conn.execute(query)
            return cursor.fetchone()[0]
        
    def get_total_usage_today(self):
        """Get the total duration of all app sessions for the current day"""
        
        query = """
        SELECT COALESCE(SUM(duration), 0)
        FROM session
        WHERE DATE(start_time) = DATE('now')
        """

        with self._get_connection() as conn:
            cursor = conn.execute(query)
            result = cursor.fetchone()
        print(result[0])
        return result[0] if result else 0
