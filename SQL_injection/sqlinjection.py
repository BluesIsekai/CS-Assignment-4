
from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

DATABASE = "users.db"


# ==========================================
# DATABASE INITIALIZATION
# ==========================================

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


# ==========================================
# ORIGINAL LOGIN PAGE
# Used by Vulnerable and Secure routes
# ==========================================

LOGIN_PAGE = """
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

        <input name="username"
               placeholder="Username"
               required>

        <input name="password"
               type="password"
               placeholder="Password"
               required>

        <button type="submit">Login</button>

    </form>

    {% if result %}
    <div class="result">
        {{ result }}
    </div>
    {% endif %}

    <p><a href="/">Home</a></p>

</div>

</body>
</html>
"""


# ==========================================
# STYLED PAGE DESIGN
# Used only by Mitigations page
# ==========================================

BASE_STYLE = """
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    body {
        background: #0b1120;
        color: #e5e7eb;
        font-family: Arial, sans-serif;
        min-height: 100vh;
    }

    nav {
        background: #111827;
        border-bottom: 1px solid #374151;
        padding: 20px 8%;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 15px;
    }

    nav h2 {
        color: white;
        font-size: 21px;
    }

    nav div {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
    }

    nav a {
        color: #9ca3af;
        text-decoration: none;
        font-size: 14px;
    }

    nav a:hover {
        color: #60a5fa;
    }

    .container {
        max-width: 950px;
        margin: 65px auto;
        padding: 0 25px;
    }

    .card {
        background: #172033;
        border: 1px solid #263449;
        border-radius: 12px;
        padding: 30px;
        margin-bottom: 22px;
    }

    h1 {
        color: white;
        font-size: 32px;
        margin-bottom: 15px;
    }

    h2 {
        color: white;
        margin-bottom: 15px;
    }

    h3 {
        color: #93c5fd;
        margin-bottom: 12px;
    }

    p {
        color: #9ca3af;
        line-height: 1.7;
        margin-bottom: 12px;
    }

    .subtitle {
        color: #9ca3af;
        font-size: 16px;
        margin-bottom: 25px;
    }

    .btn {
        display: inline-block;
        background: #2563eb;
        color: white;
        padding: 12px 20px;
        border-radius: 7px;
        text-decoration: none;
        margin: 8px 5px 0 0;
        font-size: 14px;
    }

    .btn:hover {
        background: #1d4ed8;
    }

    .btn-secondary {
        background: #374151;
    }

    .badge {
        display: inline-block;
        padding: 6px 10px;
        border-radius: 5px;
        font-size: 12px;
        margin-bottom: 15px;
    }

    .green {
        background: #143c2b;
        color: #86efac;
    }

    .blue {
        background: #172554;
        color: #93c5fd;
    }

    .code-block {
        background: #0b1120;
        border: 1px solid #374151;
        padding: 18px;
        border-radius: 8px;
        overflow-x: auto;
        margin: 15px 0;
        color: #93c5fd;
        line-height: 1.7;
        white-space: pre-wrap;
        overflow-wrap: anywhere;
    }

    code {
        background: #0b1120;
        color: #93c5fd;
        padding: 3px 6px;
        border-radius: 4px;
    }

    footer {
        text-align: center;
        padding: 30px;
        color: #6b7280;
        font-size: 13px;
    }

    @media (max-width: 600px) {
        nav {
            padding: 18px;
        }

        nav div {
            gap: 12px;
        }

        .container {
            margin: 35px auto;
        }

        h1 {
            font-size: 26px;
        }
    }
</style>
"""


# ==========================================
# MITIGATION PAGE RENDERER
# ==========================================

def render_mitigation_page(content):

    template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SQL Injection Mitigations</title>
        <meta name="viewport"
              content="width=device-width, initial-scale=1">
    """ + BASE_STYLE + """
    </head>

    <body>

        <nav>
            <h2>SQL Injection Lab</h2>

            <div>
                <a href="/">Home</a>
                <a href="/vulnerable">Vulnerable</a>
                <a href="/secure">Secure</a>
                <a href="/mitigations">Mitigations</a>
            </div>
        </nav>

        """ + content + """

        <footer>
            Cyber Security Assignment |
            SQL Injection Demonstration
        </footer>

    </body>
    </html>
    """

    return render_template_string(template)


# ==========================================
# HOME PAGE - ORIGINAL PLAIN HTML
# ==========================================

@app.route("/")
def home():

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SQL Injection Demonstration</title>
    </head>

    <body>

        <h1>SQL Injection Demonstration</h1>

        <ul>
            <li>
                <a href="/vulnerable">Vulnerable Login</a>
            </li>

            <li>
                <a href="/secure">Secure Login</a>
            </li>

            <li>
                <a href="/mitigations">Mitigation Techniques</a>
            </li>
        </ul>

    </body>
    </html>
    """


# ==========================================
# VULNERABLE LOGIN
# ==========================================

@app.route("/vulnerable", methods=["GET", "POST"])
def vulnerable():

    result = ""

    if request.method == "POST":

        username = request.form.get("username", "")
        password = request.form.get("password", "")

        conn = sqlite3.connect(DATABASE)

        # INSECURE: Direct insertion of user input
        query = (
            f"SELECT username, role FROM users "
            f"WHERE username = '{username}' "
            f"AND password = '{password}'"
        )

        print("\n--- VULNERABLE SQL QUERY ---")
        print(query)

        try:
            user = conn.execute(query).fetchone()

            if user:
                result = (
                    f"Login successful! Welcome "
                    f"{user[0]} ({user[1]})"
                )
            else:
                result = "Invalid username or password."

        except sqlite3.Error as e:

            print("Database error:", e)
            result = "SQL Error: Invalid query"

        finally:
            conn.close()

    return render_template_string(
        LOGIN_PAGE,
        mode="VULNERABLE",
        result=result
    )


# ==========================================
# SECURE LOGIN
# ==========================================

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

        try:
            user = conn.execute(
                query, (username, password)
            ).fetchone()

            if user:
                result = (
                    f"Login successful! Welcome "
                    f"{user[0]} ({user[1]})"
                )
            else:
                result = "Invalid username or password."

        finally:
            conn.close()

    return render_template_string(
        LOGIN_PAGE,
        mode="SECURE",
        result=result
    )


# ==========================================
# MITIGATION TECHNIQUES PAGE
# ==========================================

@app.route("/mitigations")
def mitigations():

    content = """
    <div class="container">

        <div class="card">

            <span class="badge blue">SECURITY GUIDE</span>

            <h1>SQL Injection Mitigation</h1>

            <p class="subtitle">
                Understanding the techniques used to prevent
                SQL Injection vulnerabilities.
            </p>

            <p>
                SQL Injection can be prevented through several
                defensive techniques. This project implements
                parameterized queries and explains three
                additional mitigation techniques.
            </p>

        </div>


        <!-- MITIGATION 1 -->

        <div class="card">

            <span class="badge green">IMPLEMENTED</span>

            <h2>01. Parameterized Queries</h2>

            <p>
                Parameterized queries separate SQL instructions
                from user-provided values by using placeholders.
            </p>

            <div class="code-block">query = (
    "SELECT username, role FROM users "
    "WHERE username = ? AND password = ?"
)

conn.execute(query, (username, password))</div>

            <p>
                The database treats the supplied values as data
                rather than executable SQL instructions.
            </p>

            <p>
                <strong>Result:</strong>
                Prevents the demonstrated authentication bypass.
            </p>

            <a href="/secure" class="btn">
                Test Secure Login
            </a>

        </div>


        <!-- MITIGATION 2 -->

        <div class="card">

            <span class="badge blue">
                THEORETICAL ALTERNATIVE
            </span>

            <h2>02. Allow-list Input Validation</h2>

            <p>
                Allow-list validation checks user input against
                predefined acceptable formats and values.
            </p>

            <p>
                For example, a username field could allow only
                letters, numbers and underscores, with a
                predefined maximum length.
            </p>

            <div class="code-block">import re

if not re.fullmatch(r"[a-zA-Z0-9_]{3,20}", username):
    print("Invalid username")</div>

            <p>
                <strong>How it helps:</strong>
                Unexpected input is rejected before it reaches
                the database.
            </p>

            <p>
                Input validation is an additional security layer,
                not a replacement for parameterized queries.
            </p>

        </div>


        <!-- MITIGATION 3 -->

        <div class="card">

            <span class="badge blue">
                THEORETICAL ALTERNATIVE
            </span>

            <h2>03. Least-Privilege Database Accounts</h2>

            <p>
                Database accounts should receive only the
                permissions necessary to perform their tasks.
            </p>

            <p>
                For example, an account used for login
                authentication should generally only need
                permission to read the relevant user records.
            </p>

            <div class="code-block">Example permissions:

Application database account:
    SELECT users

Avoid unnecessary permissions:
    DROP TABLE
    ALTER DATABASE
    CREATE USER</div>

            <p>
                <strong>How it helps:</strong>
                If an attacker successfully exploits an SQL
                Injection vulnerability, restricted permissions
                limit the potential damage.
            </p>

        </div>


        <!-- MITIGATION 4 -->

        <div class="card">

            <span class="badge blue">
                THEORETICAL ALTERNATIVE
            </span>

            <h2>04. Safe Error Handling</h2>

            <p>
                Applications should avoid exposing raw database
                errors, SQL statements or internal implementation
                details to users.
            </p>

            <div class="code-block"># User-facing response
return "An error occurred. Please try again."

# Detailed error goes to server-side logs
app.logger.exception("Database operation failed")</div>

            <p>
                <strong>How it helps:</strong>
                Prevents attackers from obtaining detailed
                information about the database structure
                and query implementation through error messages.
            </p>

        </div>


        <!-- SUMMARY -->

        <div class="card">

            <h2>Mitigation Summary</h2>

            <p>
                The techniques work together to improve
                application security.
            </p>

            <p>
                1. Parameterized Queries – Separate SQL code
                from user input.
            </p>

            <p>
                2. Allow-list Validation – Restrict input
                to expected formats.
            </p>

            <p>
                3. Least Privilege – Limit database permissions.
            </p>

            <p>
                4. Safe Error Handling – Prevent exposure
                of sensitive database information.
            </p>

            <a href="/vulnerable" class="btn btn-secondary">
                View Vulnerable Implementation
            </a>

            <a href="/secure" class="btn">
                View Secure Implementation
            </a>

        </div>

    </div>
    """

    return render_mitigation_page(content)


# ==========================================
# APPLICATION ENTRY POINT
# ==========================================

if __name__ == "__main__":

    init_db()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )
