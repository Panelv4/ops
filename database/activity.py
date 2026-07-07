from database.db import get_connection

def log_activity(module, action, message):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO activity_log (module, action, message)
        VALUES (?, ?, ?)
    """, (module, action, message))

    conn.commit()
    conn.close()
