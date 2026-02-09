import sqlite3
import os

DB_FILE = "hamster_foods.db"
SCHEMA_FILE = os.path.join("sql", "schema.sql")
SEEDS_FILE = os.path.join("sql", "seeds.sql")

def initialize_database():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print(f"Removed old database file: {DB_FILE}")

    try:
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        print(f"Successfully connected to new database: {DB_FILE}")

        with open(SCHEMA_FILE, 'r') as f:
            schema_sql = f.read()
        cursor.executescript(schema_sql)
        print(f"Successfully executed schema from: {SCHEMA_FILE}")

        with open(SEEDS_FILE, 'r') as f:
            seeds_sql = f.read()
        cursor.executescript(seeds_sql)
        print(f"Successfully executed seeds from: {SEEDS_FILE}")

        connection.commit()
        print("Database initialized and seeded successfully.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except FileNotFoundError as e:
        print(f"SQL file not found: {e}")
    finally:
        if connection:
            connection.close()
            print("Database connection closed.")

if __name__ == "__main__":
    initialize_database()
