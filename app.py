import os
import sqlite3
from pathlib import Path
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
DB = Path(__file__).parent / "grocery.db"
VERSION = os.getenv("APP_VERSION", "v1.0.0")
ENVIRONMENT = os.getenv("APP_ENVIRONMENT", "development")


def db():
    connection = sqlite3.connect(DB)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with db() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS groceries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                quantity TEXT NOT NULL,
                purchased INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)


def serialize(item):
    return {**dict(item), "purchased": bool(item["purchased"])}


@app.get("/")
def home():
    return render_template("index.html", app_version=VERSION, app_environment=ENVIRONMENT)


@app.get("/health")
def health():
    return jsonify(status="healthy")


@app.get("/api/items")
def get_items():
    with db() as connection:
        items = connection.execute(
            "SELECT * FROM groceries ORDER BY purchased, created_at DESC"
        ).fetchall()
    return jsonify([serialize(item) for item in items])


@app.post("/api/items")
def add_item():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    quantity = str(data.get("quantity", "")).strip()

    if not 1 <= len(name) <= 100:
        return jsonify(error="Item name must be 1-100 characters."), 400
    if not 1 <= len(quantity) <= 50:
        return jsonify(error="Quantity must be 1-50 characters."), 400

    with db() as connection:
        cursor = connection.execute(
            "INSERT INTO groceries (name, quantity) VALUES (?, ?)", (name, quantity)
        )
        item = connection.execute(
            "SELECT * FROM groceries WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
    return jsonify(serialize(item)), 201


@app.patch("/api/items/<int:item_id>")
def update_item(item_id):
    purchased = (request.get_json(silent=True) or {}).get("purchased")
    if not isinstance(purchased, bool):
        return jsonify(error="Purchased must be a boolean."), 400

    with db() as connection:
        cursor = connection.execute(
            "UPDATE groceries SET purchased = ? WHERE id = ?", (purchased, item_id)
        )
        if cursor.rowcount == 0:
            return jsonify(error="Item not found."), 404
    return jsonify(purchased=purchased)


@app.delete("/api/items/<int:item_id>")
def delete_item(item_id):
    with db() as connection:
        cursor = connection.execute("DELETE FROM groceries WHERE id = ?", (item_id,))
    if cursor.rowcount == 0:
        return jsonify(error="Item not found."), 404
    return jsonify(message="Item deleted.")


initialize_database()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
