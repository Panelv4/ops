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

    # USERS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        email TEXT UNIQUE,
        password TEXT,
        role TEXT DEFAULT 'user',
        company_id INTEGER
    )
    """)

    # LEADS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        score INTEGER,
        status TEXT,
        company_id INTEGER
    )
    """)

    # TICKETS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        issue TEXT,
        status TEXT,
        company_id INTEGER
    )
    """)

    # EMPLOYEES
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        role TEXT,
        company_id INTEGER
    )
    """)

    # SUBSCRIPTIONS (FIXED - SAME CONNECTION)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subscriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id INTEGER,
        plan TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()

def init_employee_tables(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id INTEGER,
        employee_code TEXT UNIQUE,
        name TEXT,
        email TEXT,
        phone TEXT,
        department TEXT,
        designation TEXT,
        status TEXT DEFAULT 'Active',
        joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER,
        login_time TIMESTAMP,
        logout_time TIMESTAMP,
        total_minutes INTEGER DEFAULT 0,
        work_date DATE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER,
        title TEXT,
        description TEXT,
        priority TEXT,
        progress INTEGER DEFAULT 0,
        status TEXT DEFAULT 'Pending',
        assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        due_date DATE
    );
    """)
