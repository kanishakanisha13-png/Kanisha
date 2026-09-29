import os
import sqlite3


# Vercel function storage is not persistent/read-write like a local machine.
# Use its writable temporary directory in production, while keeping the
# normal local SQLite file for development.
DATABASE_NAME = (
    "/tmp/pocketsmart.db"
    if os.getenv("VERCEL")
    else "pocketsmart.db"
)


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)

    # Recommendation history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recommendation_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            category TEXT NOT NULL,
            budget REAL NOT NULL,
            preferences TEXT,
            recommendations TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    connection.commit()
    connection.close()