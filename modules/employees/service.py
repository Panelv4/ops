from database.db import get_connection


class EmployeeService:

    @staticmethod
    def all():
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
        SELECT *
        FROM employees
        ORDER BY created_at DESC
        """)

        rows = [dict(r) for r in cur.fetchall()]

        conn.close()
        return rows


    @staticmethod
    def get(employee_id):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM employees WHERE id=?",
            (employee_id,)
        )

        row = cur.fetchone()

        conn.close()

        return dict(row) if row else None


    @staticmethod
    def create(data):

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO employees
        (
            employee_id,
            company_id,
            name,
            email,
            phone,
            department,
            designation,
            salary,
            status
        )
        VALUES
        (?,?,?,?,?,?,?,?,?)
        """, (

            data["employee_id"],
            data.get("company_id", 1),
            data["name"],
            data["email"],
            data.get("phone", ""),
            data.get("department", ""),
            data.get("designation", ""),
            data.get("salary", 0),
            data.get("status", "Active")

        ))

        conn.commit()

        employee = cur.lastrowid

        conn.close()

        return employee


    @staticmethod
    def update(emp_id, data):

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
        UPDATE employees
        SET
        name=?,
        email=?,
        phone=?,
        department=?,
        designation=?,
        salary=?,
        status=?
        WHERE id=?
        """, (

            data["name"],
            data["email"],
            data.get("phone", ""),
            data.get("department", ""),
            data.get("designation", ""),
            data.get("salary", 0),
            data.get("status", "Active"),
            emp_id

        ))

        conn.commit()

        conn.close()

        return True


    @staticmethod
    def delete(emp_id):

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "DELETE FROM employees WHERE id=?",
            (emp_id,)
        )

        conn.commit()

        conn.close()

        return True


    @staticmethod
    def search(keyword):

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
        SELECT *
        FROM employees
        WHERE
        name LIKE ?
        OR email LIKE ?
        OR department LIKE ?
        OR designation LIKE ?
        """, (

            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%"

        ))

        rows = [dict(r) for r in cur.fetchall()]

        conn.close()

        return rows


    @staticmethod
    def stats():

        conn = get_connection()
        cur = conn.cursor()

        stats = {}

        cur.execute("SELECT COUNT(*) FROM employees")
        stats["total"] = cur.fetchone()[0]

        cur.execute(
            "SELECT COUNT(*) FROM employees WHERE status='Active'"
        )
        stats["active"] = cur.fetchone()[0]

        cur.execute(
            "SELECT COUNT(*) FROM employees WHERE status='Inactive'"
        )
        stats["inactive"] = cur.fetchone()[0]

        cur.execute("""
        SELECT department,
               COUNT(*)
        FROM employees
        GROUP BY department
        """)

        stats["departments"] = cur.fetchall()

        conn.close()

        return stats
