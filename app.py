from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            tier TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    tier = data.get('tier', '未选择')
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password, tier) VALUES (?, ?, ?)", (username, password, tier))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"})
    except sqlite3.IntegrityError:
        return jsonify({"status": "error", "message": "账号已存在"}), 400

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT tier FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    if user:
        return jsonify({"status": "success", "tier": user[0]})
    return jsonify({"status": "error"}), 401

@app.route('/api/update_tier', methods=['POST'])
def update_tier():
    data = request.json
    username = data.get('username')
    tier = data.get('tier')
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("UPDATE users SET tier=? WHERE username=?", (tier, username))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

if __name__ == '__main__':
    init_db()
    print("TRUST-EYE 后端已启动：http://127.0.0.1:5000")
    app.run(debug=True, port=5000)