
from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

DATABASE = "users.db"


# Initialize database
def init_db():
    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    count = conn.execute(
        "SELECT COUNT(*) FROM users"
    ).fetchone()[0]

    if count == 0:
        conn.executemany("""
            INSERT INTO users (username, password, role)
            VALUES (?, ?, ?)
        """, [
            ("admin", "admin123", "Administrator"),
            ("student", "student123", "Student")
        ])

    conn.commit()
    conn.close()


PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>SQL Injection Lab</title>
    <style>
        body {
            background: #111827;
            color: white;
            font-family: Arial;
            display: flex;
            justify-content: center;
            padding-top: 80px;
        }

        .container {
            background: #1f2937;
            padding: 35px;
            border-radius: 12px;
            width: 350px;
        }

        input, button {
            width: 100%;
            padding: 12px;
            margin-top: 12px;
            box-sizing: border-box;
            border-radius: 6px;
        }

        button {
            background: #2563eb;
            color: white;
            border: none;
            cursor: pointer;
        }

        .result {
            margin-top: 20px;
            padding: 12px;
            background: #374151;
            border-radius: 6px;
        }

        a {
            color: #60a5fa;
        }
    </style>
</head>
<body>
<div class="container">
    <h2>SQL Injection Lab</h2>
    <p>Mode: {{ mode }}</p>

    <form method="POST">
        <input name="username" placeholder="Username" required>
        <input name="password" type="password"
               placeholder="Password" required>
        <button type="submit">Login</button>
    </form>

    {% if result %}
    <div class="result">{{ result }}</div>
    {% endif %}

    <p><a href="/">Home</a></p>
</div>
</body>
</html>
"""


# Homepage
@app.route("/")
def home():
    return """
    <h1>SQL Injection Demonstration</h1>
    <a href="/vulnerable">Vulnerable Login</a><br><br>
    <a href="/secure">Secure Login</a>
    """


# VULNERABLE LOGIN
@app.route("/vulnerable", methods=["GET", "POST"])
def vulnerable():

    result = ""

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        conn = sqlite3.connect(DATABASE)

        # INSECURE: Directly inserting user input into SQL
        query = f"SELECT username, role FROM users WHERE username = '{username}' AND password = '{password}'"

        print("\n--- VULNERABLE SQL QUERY ---")
        print(query)

        try:
            user = conn.execute(query).fetchone()

            if user:
                result = (
                    f"Login successful! Welcome {user[0]} ({user[1]})"
                )
            else:
                result = "Invalid username or password."

        except sqlite3.Error as e:
            result = f"SQL Error: {e}"

        finally:
            conn.close()

    return render_template_string(
        PAGE, mode="VULNERABLE", result=result
    )


# SECURE LOGIN
@app.route("/secure", methods=["GET", "POST"])
def secure():

    result = ""

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        conn = sqlite3.connect(DATABASE)

        # SECURE: Parameterized query
        query = """
            SELECT username, role FROM users
            WHERE username = ? AND password = ?
        """

        print("\n--- SECURE SQL QUERY ---")
        print(query)

        user = conn.execute(
            query, (username, password)
        ).fetchone()

        if user:
            result = (
                f"Login successful! Welcome {user[0]} ({user[1]})"
            )
        else:
            result = "Invalid username or password."

        conn.close()

    return render_template_string(
        PAGE, mode="SECURE", result=result
    )


if __name__ == "__main__":
    init_db()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )
