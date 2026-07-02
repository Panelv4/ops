from database.db import get_connection

def init_attendance():
    conn=get_connection()
    cur=conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS attendance(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER,
        company_id INTEGER,
        check_in TEXT,
        check_out TEXT,
        work_hours REAL DEFAULT 0,
        status TEXT DEFAULT 'Present',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()
