from database.db import get_connection

def init_tasks():
    conn=get_connection()
    cur=conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id INTEGER,
        employee_id INTEGER,
        title TEXT NOT NULL,
        description TEXT,
        priority TEXT DEFAULT 'Medium',
        status TEXT DEFAULT 'Pending',
        progress INTEGER DEFAULT 0,
        estimated_hours REAL DEFAULT 0,
        hours_spent REAL DEFAULT 0,
        due_date TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()
