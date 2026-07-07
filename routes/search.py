from flask import Blueprint, request, jsonify
from database.db import get_connection

search_bp = Blueprint("search", __name__)

@search_bp.route("/api/search")
def global_search():

    q = request.args.get("q","").strip()

    conn = get_connection()
    cur = conn.cursor()

    results=[]

    searches=[
        ("employees","name","Employee"),
        ("products","name","Product"),
        ("leads","name","Lead"),
        ("tasks","title","Task")
    ]

    for table,column,label in searches:
        try:
            cur.execute(
                f"SELECT {column} FROM {table} WHERE {column} LIKE ? LIMIT 5",
                (f"%{q}%",)
            )

            for row in cur.fetchall():
                results.append({
                    "module":label,
                    "name":row[0]
                })

        except:
            pass

    conn.close()

    return jsonify(results)
