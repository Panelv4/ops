from database.db import get_connection

def init_saas():
    conn = get_connection()
    cursor = conn.cursor()

    # COMPANIES
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS companies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )
    """)

    # USERS (linked to company)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        email TEXT UNIQUE,
        password TEXT,
        role TEXT DEFAULT 'user',
        company_id INTEGER,
        FOREIGN KEY(company_id) REFERENCES companies(id)
    )
    """)

    # EVERYTHING IS SCOPED BY COMPANY
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        score INTEGER,
        status TEXT,
        company_id INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        issue TEXT,
        status TEXT,
        company_id INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        role TEXT,
        company_id INTEGER
    )
    """)

    conn.commit()
    conn.close()
