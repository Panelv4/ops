from database.db import get_connection

def init_inventory():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        sku TEXT UNIQUE,
        category TEXT,
        quantity INTEGER DEFAULT 0,
        buying_price REAL DEFAULT 0,
        selling_price REAL DEFAULT 0,
        supplier TEXT,
        reorder_level INTEGER DEFAULT 5,
        company_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()
