from database.db import get_connection

def init_employees():
    conn=get_connection()
    cur=conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS employees(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id TEXT UNIQUE,
        company_id INTEGER,
        name TEXT,
        email TEXT,
        phone TEXT,
        department TEXT,
        designation TEXT,
        salary REAL DEFAULT 0,
        status TEXT DEFAULT 'Active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()
