import sqlite3
import pandas as pd

DB_PATH = "your_database.db"  # Path to your SQLite database
CSV_PATH = "UMN.csv"  # Path to your CSV file

def load_csv_to_db():
    # Load data from CSV
    df = pd.read_csv(CSV_PATH)
    
    # Connect to the database
    with sqlite3.connect(DB_PATH) as conn:
        # Write the DataFrame to a SQL table
        df.to_sql("full_data", conn, if_exists="replace", index=False)
    print("Data loaded into database successfully.")

def get_data(table_name='full_data'):
    # Connect to the database
    with sqlite3.connect(DB_PATH) as conn:
        # Query the specified table
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, conn)
    return df

def add_record(building, event, user):
    with sqlite3.connect(DB_PATH) as conn:
        # Insert a new record into the table
        query = "INSERT INTO full_data (Building, Event, User) VALUES (?, ?, ?)"
        conn.execute(query, (building, event, user))
        conn.commit()

# Load CSV data if the table does not exist
try:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("SELECT 1 FROM full_data LIMIT 1;")
except sqlite3.OperationalError:
    load_csv_to_db()  # Load data from CSV to database if table is missing
