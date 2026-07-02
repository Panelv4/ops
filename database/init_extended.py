from database.db import get_connection

def init_extended():
    conn = get_connection()
    cursor = conn.cursor()

    # CRM
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        score INTEGER,
        status TEXT DEFAULT 'new'
    )
    """)

    # Support
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        issue TEXT,
        status TEXT DEFAULT 'open'
    )
    """)

    # HR
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        role TEXT
    )
    """)

    conn.commit()
    conn.close()
