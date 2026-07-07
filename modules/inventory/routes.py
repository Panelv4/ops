from flask import Blueprint, request, jsonify
from database.db import get_connection

inventory_bp = Blueprint("inventory", __name__)

@inventory_bp.route("/api/inventory", methods=["GET"])
def list_products():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products ORDER BY id DESC")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return jsonify(rows)

@inventory_bp.route("/api/inventory", methods=["POST"])
def add_product():
    data = request.get_json(silent=True) or {}

    required = ["name"]

    for r in required:
        if r not in data or not data[r]:
            return jsonify({
                "status": "error",
                "message": f"Missing field: {r}"
            }), 400

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO products
        (name, sku, category, quantity, buying_price, selling_price,
         supplier, reorder_level, company_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["name"],
        data.get("sku"),
        data.get("category"),
        data.get("quantity", 0),
        data.get("buying_price", 0),
        data.get("selling_price", 0),
        data.get("supplier"),
        data.get("reorder_level", 5),
        data.get("company_id", 1)
    ))

    conn.commit()
    pid = cur.lastrowid
    from database.activity import log_activity
    log_activity("inventory","create","Product created")
    conn.close()

    return jsonify({"status": "success", "id": pid})


@inventory_bp.route("/api/inventory/low-stock", methods=["GET"])
def low_stock():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM products
        WHERE quantity <= reorder_level
        ORDER BY quantity ASC
    """)

    rows = [dict(r) for r in cur.fetchall()]
    conn.close()

    return jsonify(rows)
