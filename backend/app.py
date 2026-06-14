from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os
import time

app = Flask(__name__)
CORS(app)

DB_HOST = os.getenv("DATABASE_HOST", "localhost")
DB_NAME = os.getenv("DATABASE_NAME", "tododb")
DB_USER = os.getenv("DATABASE_USER", "todo_user")
DB_PASSWORD = os.getenv("DATABASE_PASSWORD", "todo_pass")
DB_PORT = os.getenv("DATABASE_PORT", "5432")


def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
    )


def wait_for_db(retries=20, delay=2):
    for _ in range(retries):
        try:
            conn = get_db_connection()
            conn.close()
            return True
        except Exception:
            time.sleep(delay)
    return False


@app.route("/health")
def health():
    return jsonify({"status": "ok", "message": "Backend is running"})


@app.route("/todos", methods=["GET"])
def get_todos():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, title, created_at FROM todos ORDER BY id DESC;")
        rows = cur.fetchall()
        cur.close()
        conn.close()

        todos = []
        for row in rows:
            todos.append({
                "id": row[0],
                "title": row[1],
                "created_at": row[2].isoformat() if row[2] else None
            })

        return jsonify(todos)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/todos", methods=["POST"])
def add_todo():
    data = request.get_json() or {}
    title = data.get("title", "").strip()

    if not title:
        return jsonify({"error": "Title is required"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO todos (title) VALUES (%s) RETURNING id;", (title,))
        todo_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Todo created", "id": todo_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    if not wait_for_db():
        print("Database not ready. Starting anyway...")

    app.run(host="0.0.0.0", port=5000, debug=True)
