import sqlite3

DB_PATH = "invites.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def setup_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS invites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message_id INTEGER UNIQUE,
        joined_user_id TEXT,
        inviter_name TEXT,
        invite_number INTEGER,
        rejoin INTEGER,
        alt INTEGER,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()