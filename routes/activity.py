from flask import Blueprint, jsonify
from database.db import get_connection

activity_bp = Blueprint("activity", __name__)

@activity_bp.route("/api/activity")
def activity():

    conn = get_connection()
    cur = conn.cursor()

    events=[]

    try:
        cur.execute("""
        SELECT name,'Employee Added' action,created_at
        FROM employees
        ORDER BY id DESC
        LIMIT 5
        """)
        events += [dict(r) for r in cur.fetchall()]
    except:
        pass

    try:
        cur.execute("""
        SELECT name,'Lead Created' action,NULL created_at
        FROM leads
        ORDER BY id DESC
        LIMIT 5
        """)
        events += [dict(r) for r in cur.fetchall()]
    except:
        pass

    try:
        cur.execute("""
        SELECT name,'Product Added' action,NULL created_at
        FROM products
        ORDER BY id DESC
        LIMIT 5
        """)
        events += [dict(r) for r in cur.fetchall()]
    except:
        pass

    conn.close()

    return jsonify(events[:10])
