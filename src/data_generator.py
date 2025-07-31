import sqlite3
import pandas as pd

class DatabaseManager:
    def __init__(self, db_path="data/placement.db"):
        # Store the path to the database file
        self.db_path = db_path
        self.conn = None  # This will hold the connection object later

    def connect_db(self):
        # Connect to the database only if not already connected
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)
            print("Yay! Database connected successfully!")  
        else:
            print("Already connected to the database.")

    def close_db(self):
        # Close the connection if it is open
        if self.conn:
            self.conn.close()
            self.conn = None
            print("Database connection is now closed. Bye!")
        else:
            print("No database connection to close.")

    def run_query(self, query, params=None):
        # This method will run any query we give it
        self.connect_db()  
        cur = self.conn.cursor()
        if params is None:
            cur.execute(query)
        else:
            cur.execute(query, params)
        self.conn.commit()  # commit changes to the database
        print("Query ran and changes committed to database!")
        return cur

    def get_data(self, query, params=None):
        # Fetch data and return as pandas DataFrame
        self.connect_db()  
        if params:
            df = pd.read_sql_query(query, self.conn, params=params)
        else:
            df = pd.read_sql_query(query, self.conn)
        print("Got data! Returning as DataFrame now.")
        return df
