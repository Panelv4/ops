from flask import Blueprint, request, jsonify, render_template
from database.db import get_connection
from datetime import datetime

attendance_bp = Blueprint("attendance_bp", __name__)

# UI PAGE
@attendance_bp.route("/attendance")
def attendance_page():
    return render_template("attendance/index.html")


# GET ALL
@attendance_bp.route("/api/attendance", methods=["GET"])
def get_all():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM attendance ORDER BY id DESC")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return jsonify(rows)


# CHECKIN
@attendance_bp.route("/api/attendance/checkin", methods=["POST"])
def checkin():
    data = request.get_json()
    employee_id = data["employee_id"]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM attendance
        WHERE employee_id=? AND check_out IS NULL
    """, (employee_id,))

    if cur.fetchone():
        conn.close()
        return jsonify({"status": "error", "message": "Already checked in"}), 400

    cur.execute("""
        INSERT INTO attendance(employee_id, company_id, check_in)
        VALUES (?, ?, ?)
    """, (
        employee_id,
        data.get("company_id", 1),
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()

    return jsonify({"status": "success"})


# CHECKOUT
@attendance_bp.route("/api/attendance/checkout/<int:employee_id>", methods=["POST"])
def checkout(employee_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM attendance
        WHERE employee_id=? AND check_out IS NULL
        ORDER BY id DESC LIMIT 1
    """, (employee_id,))

    row = cur.fetchone()

    if not row:
        conn.close()
        return jsonify({"status": "error", "message": "No active session"}), 400

    check_in = datetime.fromisoformat(row["check_in"])
    check_out = datetime.now()

    hours = (check_out - check_in).total_seconds() / 3600

    cur.execute("""
        UPDATE attendance
        SET check_out=?, work_hours=?
        WHERE id=?
    """, (
        check_out.isoformat(),
        round(hours, 2),
        row["id"]
    ))

    conn.commit()
    conn.close()

    return jsonify({"status": "success", "hours": hours})

@attendance_bp.route("/api/attendance/live", methods=["GET"])
def live_status():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT employee_id, check_in, check_out, work_hours
        FROM attendance
        ORDER BY id DESC
    """)

    rows = cur.fetchall()
    conn.close()

    active = []
    inactive = []

    for r in rows:
        if r["check_out"] is None:
            active.append(dict(r))
        else:
            inactive.append(dict(r))

    return jsonify({
        "active": active,
        "inactive": inactive,
        "active_count": len(active),
        "inactive_count": len(inactive)
    })

@attendance_bp.route("/api/attendance/analytics", methods=["GET"])
def analytics():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM attendance")
    rows = cur.fetchall()
    conn.close()

    total = len(rows)
    present = 0
    late = 0
    total_hours = 0

    for r in rows:
        if r["check_in"]:
            present += 1

        if r["check_in"] and "09:15" in r["check_in"]:
            late += 1

        if r["work_hours"]:
            total_hours += r["work_hours"]

    avg_hours = total_hours / total if total else 0

    return jsonify({
        "total_records": total,
        "present_count": present,
        "late_count": late,
        "average_hours": round(avg_hours, 2)
    })

from datetime import datetime, time

SHIFT_START = time(9, 0)
GRACE_MINUTES = 15


@attendance_bp.route("/api/attendance/advanced-analytics", methods=["GET"])
def advanced_analytics():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM attendance")
    rows = cur.fetchall()
    conn.close()

    total = len(rows)
    present = 0
    late = 0
    total_hours = 0
    productivity_score = {}

    for r in rows:
        emp = r["employee_id"]

        # --- presence ---
        if r["check_in"]:
            present += 1

        # --- real late detection ---
        if r["check_in"]:
            try:
                check_in_time = datetime.fromisoformat(r["check_in"]).time()
                grace_limit = time(
                    SHIFT_START.hour,
                    SHIFT_START.minute + GRACE_MINUTES
                )

                if check_in_time > grace_limit:
                    late += 1
            except:
                pass

        # --- hours ---
        if r["work_hours"]:
            total_hours += r["work_hours"]

            if emp not in productivity_score:
                productivity_score[emp] = 0

            productivity_score[emp] += r["work_hours"]

    avg_hours = total_hours / total if total else 0

    return jsonify({
        "total_records": total,
        "present": present,
        "late": late,
        "average_hours": round(avg_hours, 2),
        "productivity_per_employee": productivity_score
    })

@attendance_bp.route("/api/attendance/dashboard-metrics", methods=["GET"])
def dashboard_metrics():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM attendance")
    rows = cur.fetchall()
    conn.close()

    present = 0
    late = 0
    active = 0
    inactive = 0

    for r in rows:
        if r["check_in"]:
            present += 1

        if r["check_in"] and "09:15" in r["check_in"]:
            late += 1

        if r["check_out"] is None:
            active += 1
        else:
            inactive += 1

    return jsonify({
        "present": present,
        "late": late,
        "active": active,
        "inactive": inactive
    })
