import sqlite3
import pandas as pd

class DatabaseManager:
    def __init__(self, db_path="data/placement.db"):
        self.db_path = db_path
        self.conn = None

    def connect(self):
        """Establish connection to the database."""
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)

    def disconnect(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None

    def run_query(self, query, params=None):
        """Run a general SQL query (INSERT, UPDATE, DELETE)."""
        self.connect()
        cursor = self.conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        self.conn.commit()
        return cursor

    def fetch_dataframe(self, query, params=None):
        """Fetch results of a query into a pandas DataFrame."""
        self.connect()
        if params:
            df = pd.read_sql_query(query, self.conn, params=params)
        else:
            df = pd.read_sql_query(query, self.conn)
        return df
