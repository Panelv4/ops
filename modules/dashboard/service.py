from database.db import get_connection

class DashboardService:

    @staticmethod
    def summary():

        conn = get_connection()
        cur = conn.cursor()

        data = {}

        tables = {
            "employees":"employees",
            "tasks":"tasks",
            "products":"products",
            "leads":"leads",
            "finance":"finance"
        }

        for key,table in tables.items():
            try:
                cur.execute(f"SELECT COUNT(*) FROM {table}")
                data[key] = cur.fetchone()[0]
            except:
                data[key] = 0

        try:
            cur.execute("SELECT SUM(amount) FROM finance WHERE type='Income'")
            data["income"] = cur.fetchone()[0] or 0
        except:
            data["income"] = 0

        try:
            cur.execute("SELECT SUM(amount) FROM finance WHERE type='Expense'")
            data["expense"] = cur.fetchone()[0] or 0
        except:
            data["expense"] = 0

        data["balance"] = data["income"] - data["expense"]

        conn.close()

        return data

    @staticmethod
    def activity():

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT module, action, message, created_at
            FROM activity_log
            ORDER BY id DESC
            LIMIT 20
        """)

        rows = [dict(r) for r in cur.fetchall()]

        conn.close()
        return rows
